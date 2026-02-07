import { ProductService } from '../services/product.service';
import { ProductRepository } from '../repositories/product.repository';
import { CategoryRepository } from '../repositories/category.repository';
import { CreateProductDTO } from '../models/product.model';

describe('ProductService', () => {
  let productService: ProductService;
  let productRepo: ProductRepository;
  let categoryRepo: CategoryRepository;

  beforeEach(() => {
    productRepo = new ProductRepository();
    categoryRepo = new CategoryRepository();
    productService = new ProductService(productRepo, categoryRepo);
  });

  const validProduct: CreateProductDTO = {
    name: 'Test Widget',
    description: 'A great widget for testing',
    sku: 'WIDGET-001',
    price: 29.99,
    tags: ['electronics', 'gadgets'],
  };

  describe('createProduct', () => {
    it('should create a product successfully', () => {
      const product = productService.createProduct(validProduct);
      expect(product.name).toBe('Test Widget');
      expect(product.sku).toBe('WIDGET-001');
      expect(product.price).toBe(29.99);
      expect(product.isActive).toBe(true);
    });

    it('should reject duplicate SKU', () => {
      productService.createProduct(validProduct);
      expect(() => productService.createProduct(validProduct)).toThrow('already exists');
    });

    it('should reject empty name', () => {
      expect(() =>
        productService.createProduct({ ...validProduct, name: '', sku: 'NEW-001' })
      ).toThrow('name is required');
    });

    it('should reject negative price', () => {
      expect(() =>
        productService.createProduct({ ...validProduct, price: -10, sku: 'NEW-001' })
      ).toThrow('negative');
    });

    it('should reject invalid SKU format', () => {
      expect(() =>
        productService.createProduct({ ...validProduct, sku: 'INVALID SKU!' })
      ).toThrow('SKU');
    });

    it('should validate category exists', () => {
      expect(() =>
        productService.createProduct({
          ...validProduct,
          sku: 'NEW-001',
          categoryId: 'nonexistent',
        })
      ).toThrow('not found');
    });

    it('should assign product to valid category', () => {
      const category = categoryRepo.create({
        name: 'Electronics',
        description: 'Electronic devices',
      });
      const product = productService.createProduct({
        ...validProduct,
        sku: 'ELEC-001',
        categoryId: category.id,
      });
      expect(product.categoryId).toBe(category.id);
    });
  });

  describe('getProduct', () => {
    it('should return product by id', () => {
      const created = productService.createProduct(validProduct);
      const found = productService.getProduct(created.id);
      expect(found).toBeDefined();
      expect(found!.id).toBe(created.id);
    });

    it('should return null for nonexistent id', () => {
      const found = productService.getProduct('nonexistent');
      expect(found).toBeNull();
    });
  });

  describe('updateProduct', () => {
    it('should update product name', () => {
      const created = productService.createProduct(validProduct);
      const updated = productService.updateProduct(created.id, { name: 'Updated Widget' });
      expect(updated).toBeDefined();
      expect(updated!.name).toBe('Updated Widget');
    });

    it('should reject negative price update', () => {
      const created = productService.createProduct(validProduct);
      expect(() => productService.updateProduct(created.id, { price: -5 })).toThrow('negative');
    });

    it('should return null for nonexistent product', () => {
      const result = productService.updateProduct('nonexistent', { name: 'Test' });
      expect(result).toBeNull();
    });
  });

  describe('deleteProduct', () => {
    it('should delete existing product', () => {
      const created = productService.createProduct(validProduct);
      expect(productService.deleteProduct(created.id)).toBe(true);
      expect(productService.getProduct(created.id)).toBeNull();
    });

    it('should return false for nonexistent product', () => {
      expect(productService.deleteProduct('nonexistent')).toBe(false);
    });
  });

  describe('searchProducts', () => {
    beforeEach(() => {
      productService.createProduct({ ...validProduct, sku: 'W-001', name: 'Blue Widget', price: 10 });
      productService.createProduct({
        ...validProduct,
        sku: 'W-002',
        name: 'Red Widget',
        price: 25,
        tags: ['sale'],
      });
      productService.createProduct({
        ...validProduct,
        sku: 'G-001',
        name: 'Green Gadget',
        price: 50,
      });
    });

    it('should search by name', () => {
      const results = productService.searchProducts({ name: 'Widget' });
      expect(results.length).toBe(2);
    });

    it('should search by price range', () => {
      const results = productService.searchProducts({ minPrice: 20, maxPrice: 40 });
      expect(results.length).toBe(1);
      expect(results[0].name).toBe('Red Widget');
    });

    it('should search by tags', () => {
      const results = productService.searchProducts({ tags: ['sale'] });
      expect(results.length).toBe(1);
    });
  });

  describe('tags management', () => {
    it('should add tags to product', () => {
      const created = productService.createProduct(validProduct);
      const updated = productService.addTags(created.id, ['new-tag']);
      expect(updated!.tags).toContain('new-tag');
      expect(updated!.tags).toContain('electronics');
    });

    it('should not duplicate existing tags', () => {
      const created = productService.createProduct(validProduct);
      const updated = productService.addTags(created.id, ['electronics', 'new-tag']);
      const electronicsCount = updated!.tags.filter(t => t === 'electronics').length;
      expect(electronicsCount).toBe(1);
    });

    it('should remove tags from product', () => {
      const created = productService.createProduct(validProduct);
      const updated = productService.removeTags(created.id, ['electronics']);
      expect(updated!.tags).not.toContain('electronics');
      expect(updated!.tags).toContain('gadgets');
    });
  });

  describe('activation', () => {
    it('should deactivate product', () => {
      const created = productService.createProduct(validProduct);
      const deactivated = productService.deactivateProduct(created.id);
      expect(deactivated!.isActive).toBe(false);
    });

    it('should activate product', () => {
      const created = productService.createProduct(validProduct);
      productService.deactivateProduct(created.id);
      const activated = productService.activateProduct(created.id);
      expect(activated!.isActive).toBe(true);
    });
  });
});

