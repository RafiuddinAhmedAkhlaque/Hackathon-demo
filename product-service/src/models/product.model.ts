export interface Product {
  id: string;
  name: string;
  description: string;
  sku: string;
  price: number;
  categoryId: string | null;
  tags: string[];
  imageUrl: string | null;
  weight: number | null; // in grams
  dimensions: Dimensions | null;
  isActive: boolean;
  stockQuantity: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface Dimensions {
  length: number;
  width: number;
  height: number;
  unit: 'cm' | 'in';
}

export interface CreateProductDTO {
  name: string;
  description: string;
  sku: string;
  price: number;
  categoryId?: string;
  tags?: string[];
  imageUrl?: string;
  weight?: number;
  dimensions?: Dimensions;
}

export interface UpdateProductDTO {
  name?: string;
  description?: string;
  price?: number;
  categoryId?: string | null;
  tags?: string[];
  imageUrl?: string | null;
  weight?: number | null;
  dimensions?: Dimensions | null;
  isActive?: boolean;
}

export interface ProductSearchQuery {
  name?: string;
  categoryId?: string;
  minPrice?: number;
  maxPrice?: number;
  tags?: string[];
  isActive?: boolean;
}

