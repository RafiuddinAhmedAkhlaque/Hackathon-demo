import { v4 as uuidv4 } from 'uuid';
import {
  PriceRule,
  CreatePriceRuleDTO,
  UpdatePriceRuleDTO,
  PriceCalculationResult,
} from '../models/price-rule.model';
import { Product } from '../models/product.model';
import { ProductRepository } from '../repositories/product.repository';

export class PricingService {
  private rules: Map<string, PriceRule> = new Map();

  constructor(private productRepo: ProductRepository) {}

  createRule(data: CreatePriceRuleDTO): PriceRule {
    this.validateRuleData(data);

    const rule: PriceRule = {
      id: uuidv4(),
      name: data.name,
      description: data.description,
      type: data.type,
      value: data.value,
      productId: data.productId || null,
      categoryId: data.categoryId || null,
      minQuantity: data.minQuantity || 1,
      maxQuantity: data.maxQuantity || null,
      startDate: data.startDate || new Date(),
      endDate: data.endDate || null,
      isActive: true,
      priority: data.priority || 0,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.rules.set(rule.id, rule);
    return rule;
  }

  getRule(id: string): PriceRule | null {
    return this.rules.get(id) || null;
  }

  updateRule(id: string, data: UpdatePriceRuleDTO): PriceRule | null {
    const rule = this.rules.get(id);
    if (!rule) return null;

    const updated: PriceRule = {
      ...rule,
      ...Object.fromEntries(
        Object.entries(data).filter(([_, v]) => v !== undefined)
      ),
      updatedAt: new Date(),
    };

    this.rules.set(id, updated);
    return updated;
  }

  deleteRule(id: string): boolean {
    return this.rules.delete(id);
  }

  calculatePrice(productId: string, quantity: number = 1): PriceCalculationResult {
    const product = this.productRepo.getById(productId);
    if (!product) {
      throw new Error(`Product '${productId}' not found`);
    }

    const applicableRules = this.getApplicableRules(product, quantity);
    let finalPrice = product.price;
    const appliedRuleIds: string[] = [];

    // Apply rules in priority order (highest first)
    for (const rule of applicableRules) {
      const newPrice = this.applyRule(finalPrice, rule, quantity);
      if (newPrice !== finalPrice) {
        finalPrice = newPrice;
        appliedRuleIds.push(rule.id);
      }
    }

    // Ensure price doesn't go below 0
    finalPrice = Math.max(0, finalPrice);
    finalPrice = Math.round(finalPrice * 100) / 100;

    return {
      originalPrice: product.price,
      finalPrice,
      discount: Math.round((product.price - finalPrice) * 100) / 100,
      appliedRules: appliedRuleIds,
    };
  }

  getActiveRules(): PriceRule[] {
    const now = new Date();
    return Array.from(this.rules.values()).filter(
      rule =>
        rule.isActive &&
        rule.startDate <= now &&
        (rule.endDate === null || rule.endDate >= now)
    );
  }

  getRulesForProduct(productId: string): PriceRule[] {
    return Array.from(this.rules.values()).filter(
      rule => rule.productId === productId || rule.productId === null
    );
  }

  private getApplicableRules(product: Product, quantity: number): PriceRule[] {
    const now = new Date();

    return Array.from(this.rules.values())
      .filter(rule => {
        if (!rule.isActive) return false;
        if (rule.startDate > now) return false;
        if (rule.endDate && rule.endDate < now) return false;
        if (rule.minQuantity > quantity) return false;
        if (rule.maxQuantity !== null && rule.maxQuantity < quantity) return false;

        // Check product/category match
        if (rule.productId && rule.productId !== product.id) return false;
        if (rule.categoryId && rule.categoryId !== product.categoryId) return false;

        return true;
      })
      .sort((a, b) => b.priority - a.priority);
  }

  private applyRule(currentPrice: number, rule: PriceRule, quantity: number): number {
    switch (rule.type) {
      case 'percentage_discount':
        return currentPrice * (1 - rule.value / 100);
      case 'fixed_discount':
        return currentPrice - rule.value;
      case 'fixed_price':
        return rule.value;
      case 'bulk_discount':
        return currentPrice * (1 - (rule.value * quantity) / 100);
      default:
        return currentPrice;
    }
  }

  private validateRuleData(data: CreatePriceRuleDTO): void {
    if (!data.name || data.name.trim().length === 0) {
      throw new Error('Rule name is required');
    }
    if (data.value < 0) {
      throw new Error('Rule value cannot be negative');
    }
    if (data.type === 'percentage_discount' && data.value > 100) {
      throw new Error('Percentage discount cannot exceed 100%');
    }
  }
}

