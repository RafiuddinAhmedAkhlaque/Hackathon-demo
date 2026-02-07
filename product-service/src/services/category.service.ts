import { Category, CreateCategoryDTO, UpdateCategoryDTO, CategoryTree } from '../models/category.model';
import { CategoryRepository } from '../repositories/category.repository';
import { ProductRepository } from '../repositories/product.repository';

export class CategoryService {
  constructor(
    private categoryRepo: CategoryRepository,
    private productRepo: ProductRepository
  ) {}

  createCategory(data: CreateCategoryDTO): Category {
    this.validateCategoryData(data);

    // Validate parent exists if provided
    if (data.parentId) {
      const parent = this.categoryRepo.getById(data.parentId);
      if (!parent) {
        throw new Error(`Parent category '${data.parentId}' not found`);
      }
    }

    return this.categoryRepo.create(data);
  }

  getCategory(id: string): Category | null {
    return this.categoryRepo.getById(id);
  }

  getCategoryBySlug(slug: string): Category | null {
    return this.categoryRepo.getBySlug(slug);
  }

  updateCategory(id: string, data: UpdateCategoryDTO): Category | null {
    const existing = this.categoryRepo.getById(id);
    if (!existing) return null;

    if (data.name) {
      if (data.name.trim().length === 0) {
        throw new Error('Category name cannot be empty');
      }
      if (data.name.length > 100) {
        throw new Error('Category name must be 100 characters or less');
      }
    }

    // Prevent circular parent reference
    if (data.parentId !== undefined && data.parentId !== null) {
      if (data.parentId === id) {
        throw new Error('Category cannot be its own parent');
      }
      const parent = this.categoryRepo.getById(data.parentId);
      if (!parent) {
        throw new Error(`Parent category '${data.parentId}' not found`);
      }
      if (this.isDescendant(data.parentId, id)) {
        throw new Error('Circular parent reference detected');
      }
    }

    return this.categoryRepo.update(id, data);
  }

  deleteCategory(id: string): boolean {
    // Check if category has products
    const products = this.productRepo.getByCategory(id);
    if (products.length > 0) {
      throw new Error('Cannot delete category with associated products');
    }

    return this.categoryRepo.delete(id);
  }

  getCategoryTree(): CategoryTree[] {
    return this.categoryRepo.getCategoryTree();
  }

  getSubcategories(parentId: string): Category[] {
    return this.categoryRepo.getChildren(parentId);
  }

  getRootCategories(): Category[] {
    return this.categoryRepo.getRootCategories();
  }

  listAll(): Category[] {
    return this.categoryRepo.listAll();
  }

  private isDescendant(ancestorId: string, descendantId: string): boolean {
    const children = this.categoryRepo.getChildren(descendantId);
    for (const child of children) {
      if (child.id === ancestorId) return true;
      if (this.isDescendant(ancestorId, child.id)) return true;
    }
    return false;
  }

  private validateCategoryData(data: CreateCategoryDTO): void {
    if (!data.name || data.name.trim().length === 0) {
      throw new Error('Category name is required');
    }
    if (data.name.length > 100) {
      throw new Error('Category name must be 100 characters or less');
    }
    if (!data.description || data.description.trim().length === 0) {
      throw new Error('Category description is required');
    }
  }
}

