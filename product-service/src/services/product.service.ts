import { Product, CreateProductDTO, UpdateProductDTO, ProductSearchQuery } from '../models/product.model';
import { ProductRepository } from '../repositories/product.repository';
import { CategoryRepository } from '../repositories/category.repository';

export class ProductService {
  constructor(
    private productRepo: ProductRepository,
    private categoryRepo: CategoryRepository
  ) {}

  createProduct(data: CreateProductDTO): Product {
    // Validate
    this.validateProductData(data);

    // Verify category exists if provided
    if (data.categoryId) {
      const category = this.categoryRepo.getById(data.categoryId);
      if (!category) {
        throw new Error(`Category '${data.categoryId}' not found`);
      }
      if (!category.isActive) {
        throw new Error(`Category '${data.categoryId}' is not active`);
      }
    }

    // Check SKU uniqueness
    if (this.productRepo.getBySku(data.sku)) {
      throw new Error(`Product with SKU '${data.sku}' already exists`);
    }

    return this.productRepo.create(data);
  }

  getProduct(id: string): Product | null {
    return this.productRepo.getById(id);
  }

  getProductBySku(sku: string): Product | null {
    return this.productRepo.getBySku(sku);
  }

  updateProduct(id: string, data: UpdateProductDTO): Product | null {
    const existing = this.productRepo.getById(id);
    if (!existing) return null;

    // Validate price if provided
    if (data.price !== undefined && data.price < 0) {
      throw new Error('Price cannot be negative');
    }

    // Verify category if being changed
    if (data.categoryId !== undefined && data.categoryId !== null) {
      const category = this.categoryRepo.getById(data.categoryId);
      if (!category) {
        throw new Error(`Category '${data.categoryId}' not found`);
      }
    }

    return this.productRepo.update(id, data);
  }

  deleteProduct(id: string): boolean {
    return this.productRepo.delete(id);
  }

  searchProducts(query: ProductSearchQuery): Product[] {
    return this.productRepo.search(query);
  }

  listProducts(skip: number = 0, limit: number = 100): Product[] {
    return this.productRepo.listAll(skip, limit);
  }

  deactivateProduct(id: string): Product | null {
    return this.productRepo.update(id, { isActive: false });
  }

  activateProduct(id: string): Product | null {
    return this.productRepo.update(id, { isActive: true });
  }

  getProductsByCategory(categoryId: string): Product[] {
    return this.productRepo.getByCategory(categoryId);
  }

  addTags(id: string, tags: string[]): Product | null {
    const product = this.productRepo.getById(id);
    if (!product) return null;

    const uniqueTags = [...new Set([...product.tags, ...tags])];
    return this.productRepo.update(id, { tags: uniqueTags });
  }

  removeTags(id: string, tags: string[]): Product | null {
    const product = this.productRepo.getById(id);
    if (!product) return null;

    const remaining = product.tags.filter(t => !tags.includes(t));
    return this.productRepo.update(id, { tags: remaining });
  }

  private validateProductData(data: CreateProductDTO): void {
    if (!data.name || data.name.trim().length === 0) {
      throw new Error('Product name is required');
    }
    if (data.name.length > 200) {
      throw new Error('Product name must be 200 characters or less');
    }
    if (!data.sku || data.sku.trim().length === 0) {
      throw new Error('SKU is required');
    }
    if (!/^[A-Za-z0-9\-_]+$/.test(data.sku)) {
      throw new Error('SKU can only contain letters, numbers, hyphens, and underscores');
    }
    if (data.price < 0) {
      throw new Error('Price cannot be negative');
    }
    if (data.weight !== undefined && data.weight < 0) {
      throw new Error('Weight cannot be negative');
    }
  }
}

