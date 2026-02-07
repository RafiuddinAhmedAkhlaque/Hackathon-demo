import { PricingService } from '../services/pricing.service';
import { ProductRepository } from '../repositories/product.repository';

describe('PricingService', () => {
  let pricingService: PricingService;
  let productRepo: ProductRepository;
  let testProductId: string;

  beforeEach(() => {
    productRepo = new ProductRepository();
    pricingService = new PricingService(productRepo);

    // Create a test product
    const product = productRepo.create({
      name: 'Test Product',
      description: 'A test product',
      sku: 'TEST-001',
      price: 100,
    });
    testProductId = product.id;
  });

  describe('createRule', () => {
    it('should create a price rule successfully', () => {
      const rule = pricingService.createRule({
        name: '10% Off Everything',
        description: 'Site-wide 10% discount',
        type: 'percentage_discount',
        value: 10,
      });
      expect(rule.name).toBe('10% Off Everything');
      expect(rule.type).toBe('percentage_discount');
      expect(rule.isActive).toBe(true);
    });

    it('should reject empty name', () => {
      expect(() =>
        pricingService.createRule({
          name: '',
          description: 'Test',
          type: 'percentage_discount',
          value: 10,
        })
      ).toThrow('name is required');
    });

    it('should reject negative value', () => {
      expect(() =>
        pricingService.createRule({
          name: 'Bad Rule',
          description: 'Test',
          type: 'fixed_discount',
          value: -5,
        })
      ).toThrow('negative');
    });

    it('should reject percentage discount over 100', () => {
      expect(() =>
        pricingService.createRule({
          name: 'Over 100%',
          description: 'Test',
          type: 'percentage_discount',
          value: 150,
        })
      ).toThrow('100%');
    });
  });

  describe('calculatePrice', () => {
    it('should return original price with no rules', () => {
      const result = pricingService.calculatePrice(testProductId);
      expect(result.originalPrice).toBe(100);
      expect(result.finalPrice).toBe(100);
      expect(result.discount).toBe(0);
      expect(result.appliedRules).toHaveLength(0);
    });

    it('should apply percentage discount', () => {
      pricingService.createRule({
        name: '20% Off',
        description: 'Discount',
        type: 'percentage_discount',
        value: 20,
      });
      const result = pricingService.calculatePrice(testProductId);
      expect(result.finalPrice).toBe(80);
      expect(result.discount).toBe(20);
    });

    it('should apply fixed discount', () => {
      pricingService.createRule({
        name: '$15 Off',
        description: 'Discount',
        type: 'fixed_discount',
        value: 15,
      });
      const result = pricingService.calculatePrice(testProductId);
      expect(result.finalPrice).toBe(85);
      expect(result.discount).toBe(15);
    });

    it('should apply fixed price rule', () => {
      pricingService.createRule({
        name: 'Sale Price',
        description: 'Special sale',
        type: 'fixed_price',
        value: 49.99,
      });
      const result = pricingService.calculatePrice(testProductId);
      expect(result.finalPrice).toBe(49.99);
    });

    it('should not let price go below zero', () => {
      pricingService.createRule({
        name: 'Huge Discount',
        description: 'Too much off',
        type: 'fixed_discount',
        value: 200,
      });
      const result = pricingService.calculatePrice(testProductId);
      expect(result.finalPrice).toBe(0);
    });

    it('should apply rules by priority', () => {
      pricingService.createRule({
        name: '10% Off',
        description: 'Lower priority',
        type: 'percentage_discount',
        value: 10,
        priority: 1,
      });
      pricingService.createRule({
        name: '$5 Off',
        description: 'Higher priority',
        type: 'fixed_discount',
        value: 5,
        priority: 10,
      });
      const result = pricingService.calculatePrice(testProductId);
      // $5 off first (priority 10) -> $95, then 10% off -> $85.50
      expect(result.finalPrice).toBe(85.5);
      expect(result.appliedRules).toHaveLength(2);
    });

    it('should respect quantity-based rules', () => {
      pricingService.createRule({
        name: 'Bulk Discount',
        description: 'Buy 5+ for discount',
        type: 'percentage_discount',
        value: 15,
        minQuantity: 5,
      });
      // Quantity 1 - rule should not apply
      const result1 = pricingService.calculatePrice(testProductId, 1);
      expect(result1.finalPrice).toBe(100);

      // Quantity 5 - rule should apply
      const result5 = pricingService.calculatePrice(testProductId, 5);
      expect(result5.finalPrice).toBe(85);
    });

    it('should throw for nonexistent product', () => {
      expect(() => pricingService.calculatePrice('nonexistent')).toThrow('not found');
    });

    it('should only apply product-specific rules to matching products', () => {
      const otherProduct = productRepo.create({
        name: 'Other Product',
        description: 'Another product',
        sku: 'OTHER-001',
        price: 50,
      });
      pricingService.createRule({
        name: 'Product Specific',
        description: 'Only for test product',
        type: 'percentage_discount',
        value: 25,
        productId: testProductId,
      });
      // Test product should get discount
      const result1 = pricingService.calculatePrice(testProductId);
      expect(result1.finalPrice).toBe(75);

      // Other product should not
      const result2 = pricingService.calculatePrice(otherProduct.id);
      expect(result2.finalPrice).toBe(50);
    });
  });

  describe('rule management', () => {
    it('should update a rule', () => {
      const rule = pricingService.createRule({
        name: 'Test Rule',
        description: 'Test',
        type: 'percentage_discount',
        value: 10,
      });
      const updated = pricingService.updateRule(rule.id, { value: 20 });
      expect(updated!.value).toBe(20);
    });

    it('should delete a rule', () => {
      const rule = pricingService.createRule({
        name: 'Test Rule',
        description: 'Test',
        type: 'percentage_discount',
        value: 10,
      });
      expect(pricingService.deleteRule(rule.id)).toBe(true);
      expect(pricingService.getRule(rule.id)).toBeNull();
    });

    it('should get active rules only', () => {
      const rule = pricingService.createRule({
        name: 'Active Rule',
        description: 'Test',
        type: 'percentage_discount',
        value: 10,
      });
      pricingService.createRule({
        name: 'Future Rule',
        description: 'Test',
        type: 'percentage_discount',
        value: 20,
        startDate: new Date(Date.now() + 86400000), // tomorrow
      });
      const activeRules = pricingService.getActiveRules();
      expect(activeRules.length).toBe(1);
      expect(activeRules[0].id).toBe(rule.id);
    });
  });
});

