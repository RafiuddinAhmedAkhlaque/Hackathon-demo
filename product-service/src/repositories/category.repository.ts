import { v4 as uuidv4 } from 'uuid';
import { Category, CreateCategoryDTO, UpdateCategoryDTO, CategoryTree } from '../models/category.model';

export class CategoryRepository {
  private categories: Map<string, Category> = new Map();
  private slugIndex: Map<string, string> = new Map(); // slug -> categoryId

  create(data: CreateCategoryDTO): Category {
    const slug = this.generateSlug(data.name);
    if (this.slugIndex.has(slug)) {
      throw new Error(`Category with slug '${slug}' already exists`);
    }

    const category: Category = {
      id: uuidv4(),
      name: data.name,
      description: data.description,
      parentId: data.parentId || null,
      slug,
      isActive: true,
      sortOrder: data.sortOrder || 0,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.categories.set(category.id, category);
    this.slugIndex.set(slug, category.id);
    return category;
  }

  getById(id: string): Category | null {
    return this.categories.get(id) || null;
  }

  getBySlug(slug: string): Category | null {
    const id = this.slugIndex.get(slug);
    if (id) return this.categories.get(id) || null;
    return null;
  }

  update(id: string, data: UpdateCategoryDTO): Category | null {
    const category = this.categories.get(id);
    if (!category) return null;

    const updated: Category = {
      ...category,
      ...Object.fromEntries(
        Object.entries(data).filter(([_, v]) => v !== undefined)
      ),
      updatedAt: new Date(),
    };

    // Update slug if name changed
    if (data.name && data.name !== category.name) {
      this.slugIndex.delete(category.slug);
      updated.slug = this.generateSlug(data.name);
      this.slugIndex.set(updated.slug, id);
    }

    this.categories.set(id, updated);
    return updated;
  }

  delete(id: string): boolean {
    const category = this.categories.get(id);
    if (!category) return false;

    // Check for children
    const children = this.getChildren(id);
    if (children.length > 0) {
      throw new Error('Cannot delete category with child categories');
    }

    this.slugIndex.delete(category.slug);
    this.categories.delete(id);
    return true;
  }

  getChildren(parentId: string): Category[] {
    return Array.from(this.categories.values())
      .filter(c => c.parentId === parentId)
      .sort((a, b) => a.sortOrder - b.sortOrder);
  }

  getRootCategories(): Category[] {
    return Array.from(this.categories.values())
      .filter(c => c.parentId === null)
      .sort((a, b) => a.sortOrder - b.sortOrder);
  }

  getCategoryTree(): CategoryTree[] {
    const roots = this.getRootCategories();
    return roots.map(root => this.buildTree(root));
  }

  listAll(): Category[] {
    return Array.from(this.categories.values())
      .sort((a, b) => a.sortOrder - b.sortOrder);
  }

  private buildTree(category: Category): CategoryTree {
    const children = this.getChildren(category.id);
    return {
      ...category,
      children: children.map(child => this.buildTree(child)),
    };
  }

  private generateSlug(name: string): string {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
  }
}

