import { v4 as uuidv4 } from 'uuid';
import { Product, CreateProductDTO, UpdateProductDTO, ProductSearchQuery } from '../models/product.model';

export class ProductRepository {
  private products: Map<string, Product> = new Map();
  private skuIndex: Map<string, string> = new Map(); // sku -> productId

  create(data: CreateProductDTO): Product {
    if (this.skuIndex.has(data.sku)) {
      throw new Error(`Product with SKU '${data.sku}' already exists`);
    }

    const product: Product = {
      id: uuidv4(),
      name: data.name,
      description: data.description,
      sku: data.sku,
      price: data.price,
      categoryId: data.categoryId || null,
      tags: data.tags || [],
      imageUrl: data.imageUrl || null,
      weight: data.weight || null,
      dimensions: data.dimensions || null,
      isActive: true,
      stockQuantity: 0,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.products.set(product.id, product);
    this.skuIndex.set(product.sku, product.id);
    return product;
  }

  getById(id: string): Product | null {
    return this.products.get(id) || null;
  }

  getBySku(sku: string): Product | null {
    const id = this.skuIndex.get(sku);
    if (id) return this.products.get(id) || null;
    return null;
  }

  update(id: string, data: UpdateProductDTO): Product | null {
    const product = this.products.get(id);
    if (!product) return null;

    const updated: Product = {
      ...product,
      ...Object.fromEntries(
        Object.entries(data).filter(([_, v]) => v !== undefined)
      ),
      updatedAt: new Date(),
    };

    this.products.set(id, updated);
    return updated;
  }

  delete(id: string): boolean {
    const product = this.products.get(id);
    if (!product) return false;

    this.skuIndex.delete(product.sku);
    this.products.delete(id);
    return true;
  }

  search(query: ProductSearchQuery): Product[] {
    let results = Array.from(this.products.values());

    if (query.name) {
      const searchName = query.name.toLowerCase();
      results = results.filter(p =>
        p.name.toLowerCase().includes(searchName)
      );
    }

    if (query.categoryId) {
      results = results.filter(p => p.categoryId === query.categoryId);
    }

    if (query.minPrice !== undefined) {
      results = results.filter(p => p.price >= query.minPrice!);
    }

    if (query.maxPrice !== undefined) {
      results = results.filter(p => p.price <= query.maxPrice!);
    }

    if (query.tags && query.tags.length > 0) {
      results = results.filter(p =>
        query.tags!.some(tag => p.tags.includes(tag))
      );
    }

    if (query.isActive !== undefined) {
      results = results.filter(p => p.isActive === query.isActive);
    }

    return results;
  }

  listAll(skip: number = 0, limit: number = 100): Product[] {
    return Array.from(this.products.values()).slice(skip, skip + limit);
  }

  count(): number {
    return this.products.size;
  }

  getByCategory(categoryId: string): Product[] {
    return Array.from(this.products.values()).filter(
      p => p.categoryId === categoryId
    );
  }
}

