export interface PriceRule {
  id: string;
  name: string;
  description: string;
  type: PriceRuleType;
  value: number; // percentage or fixed amount
  productId: string | null; // null means applies to all
  categoryId: string | null; // null means applies to all
  minQuantity: number;
  maxQuantity: number | null;
  startDate: Date;
  endDate: Date | null;
  isActive: boolean;
  priority: number; // higher = applied first
  createdAt: Date;
  updatedAt: Date;
}

export type PriceRuleType = 'percentage_discount' | 'fixed_discount' | 'fixed_price' | 'bulk_discount';

export interface CreatePriceRuleDTO {
  name: string;
  description: string;
  type: PriceRuleType;
  value: number;
  productId?: string;
  categoryId?: string;
  minQuantity?: number;
  maxQuantity?: number;
  startDate?: Date;
  endDate?: Date;
  priority?: number;
}

export interface UpdatePriceRuleDTO {
  name?: string;
  description?: string;
  value?: number;
  isActive?: boolean;
  minQuantity?: number;
  maxQuantity?: number;
  endDate?: Date | null;
  priority?: number;
}

export interface PriceCalculationResult {
  originalPrice: number;
  finalPrice: number;
  discount: number;
  appliedRules: string[]; // rule IDs
}

