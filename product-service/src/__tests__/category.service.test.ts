import { CategoryService } from '../services/category.service';
import { CategoryRepository } from '../repositories/category.repository';
import { ProductRepository } from '../repositories/product.repository';

describe('CategoryService', () => {
  let categoryService: CategoryService;
  let categoryRepo: CategoryRepository;
  let productRepo: ProductRepository;

  beforeEach(() => {
    categoryRepo = new CategoryRepository();
    productRepo = new ProductRepository();
    categoryService = new CategoryService(categoryRepo, productRepo);
  });

  describe('createCategory', () => {
    it('should create a category successfully', () => {
      const category = categoryService.createCategory({
        name: 'Electronics',
        description: 'Electronic devices and accessories',
      });
      expect(category.name).toBe('Electronics');
      expect(category.slug).toBe('electronics');
      expect(category.isActive).toBe(true);
    });

    it('should reject empty name', () => {
      expect(() =>
        categoryService.createCategory({ name: '', description: 'Test' })
      ).toThrow('name is required');
    });

    it('should reject empty description', () => {
      expect(() =>
        categoryService.createCategory({ name: 'Test', description: '' })
      ).toThrow('description is required');
    });

    it('should reject name exceeding max length', () => {
      expect(() =>
        categoryService.createCategory({
          name: 'A'.repeat(101),
          description: 'Test',
        })
      ).toThrow('100 characters');
    });

    it('should create subcategory with valid parent', () => {
      const parent = categoryService.createCategory({
        name: 'Electronics',
        description: 'All electronics',
      });
      const child = categoryService.createCategory({
        name: 'Phones',
        description: 'Mobile phones',
        parentId: parent.id,
      });
      expect(child.parentId).toBe(parent.id);
    });

    it('should reject invalid parent id', () => {
      expect(() =>
        categoryService.createCategory({
          name: 'Test',
          description: 'Test',
          parentId: 'nonexistent',
        })
      ).toThrow('not found');
    });
  });

  describe('getCategory', () => {
    it('should get category by id', () => {
      const created = categoryService.createCategory({
        name: 'Electronics',
        description: 'Electronic items',
      });
      const found = categoryService.getCategory(created.id);
      expect(found).toBeDefined();
      expect(found!.id).toBe(created.id);
    });

    it('should get category by slug', () => {
      categoryService.createCategory({
        name: 'Home & Garden',
        description: 'Home items',
      });
      const found = categoryService.getCategoryBySlug('home--garden');
      expect(found).toBeDefined();
    });

    it('should return null for nonexistent id', () => {
      expect(categoryService.getCategory('nonexistent')).toBeNull();
    });
  });

  describe('updateCategory', () => {
    it('should update category name', () => {
      const created = categoryService.createCategory({
        name: 'Electronics',
        description: 'Electronic items',
      });
      const updated = categoryService.updateCategory(created.id, {
        name: 'Consumer Electronics',
      });
      expect(updated!.name).toBe('Consumer Electronics');
    });

    it('should prevent self-referencing parent', () => {
      const created = categoryService.createCategory({
        name: 'Electronics',
        description: 'Electronic items',
      });
      expect(() =>
        categoryService.updateCategory(created.id, { parentId: created.id })
      ).toThrow('own parent');
    });

    it('should return null for nonexistent category', () => {
      expect(categoryService.updateCategory('nonexistent', { name: 'Test' })).toBeNull();
    });
  });

  describe('deleteCategory', () => {
    it('should delete category without products', () => {
      const created = categoryService.createCategory({
        name: 'Electronics',
        description: 'Electronic items',
      });
      expect(categoryService.deleteCategory(created.id)).toBe(true);
    });

    it('should prevent deleting category with products', () => {
      const category = categoryService.createCategory({
        name: 'Electronics',
        description: 'Electronic items',
      });
      productRepo.create({
        name: 'Phone',
        description: 'A phone',
        sku: 'PHONE-001',
        price: 999,
        categoryId: category.id,
      });
      expect(() => categoryService.deleteCategory(category.id)).toThrow(
        'associated products'
      );
    });

    it('should prevent deleting category with children', () => {
      const parent = categoryService.createCategory({
        name: 'Electronics',
        description: 'All electronics',
      });
      categoryService.createCategory({
        name: 'Phones',
        description: 'Mobile phones',
        parentId: parent.id,
      });
      expect(() => categoryService.deleteCategory(parent.id)).toThrow('child categories');
    });
  });

  describe('getCategoryTree', () => {
    it('should build correct tree structure', () => {
      const root = categoryService.createCategory({
        name: 'Electronics',
        description: 'All electronics',
      });
      categoryService.createCategory({
        name: 'Phones',
        description: 'Mobile phones',
        parentId: root.id,
      });
      categoryService.createCategory({
        name: 'Laptops',
        description: 'Laptop computers',
        parentId: root.id,
      });

      const tree = categoryService.getCategoryTree();
      expect(tree.length).toBe(1);
      expect(tree[0].children.length).toBe(2);
    });

    it('should return empty array with no categories', () => {
      const tree = categoryService.getCategoryTree();
      expect(tree).toEqual([]);
    });
  });

  describe('getSubcategories', () => {
    it('should return direct children only', () => {
      const root = categoryService.createCategory({
        name: 'Electronics',
        description: 'All electronics',
      });
      const phones = categoryService.createCategory({
        name: 'Phones',
        description: 'Phones',
        parentId: root.id,
      });
      categoryService.createCategory({
        name: 'Smartphones',
        description: 'Smart phones',
        parentId: phones.id,
      });

      const children = categoryService.getSubcategories(root.id);
      expect(children.length).toBe(1);
      expect(children[0].name).toBe('Phones');
    });
  });
});

