import { Router, Request, Response } from 'express';
import { CategoryService } from '../services/category.service';
import { CategoryRepository } from '../repositories/category.repository';
import { ProductRepository } from '../repositories/product.repository';

const categoryRepo = new CategoryRepository();
const productRepo = new ProductRepository();
const categoryService = new CategoryService(categoryRepo, productRepo);

export const categoryRouter = Router();

categoryRouter.post('/', (req: Request, res: Response) => {
  try {
    const category = categoryService.createCategory(req.body);
    res.status(201).json(category);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

categoryRouter.get('/', (_req: Request, res: Response) => {
  const categories = categoryService.listAll();
  res.json(categories);
});

categoryRouter.get('/tree', (_req: Request, res: Response) => {
  const tree = categoryService.getCategoryTree();
  res.json(tree);
});

categoryRouter.get('/roots', (_req: Request, res: Response) => {
  const roots = categoryService.getRootCategories();
  res.json(roots);
});

categoryRouter.get('/:id', (req: Request, res: Response) => {
  const category = categoryService.getCategory(req.params.id);
  if (!category) {
    res.status(404).json({ error: 'Category not found' });
    return;
  }
  res.json(category);
});

categoryRouter.get('/:id/subcategories', (req: Request, res: Response) => {
  const subcategories = categoryService.getSubcategories(req.params.id);
  res.json(subcategories);
});

categoryRouter.put('/:id', (req: Request, res: Response) => {
  try {
    const category = categoryService.updateCategory(req.params.id, req.body);
    if (!category) {
      res.status(404).json({ error: 'Category not found' });
      return;
    }
    res.json(category);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

categoryRouter.delete('/:id', (req: Request, res: Response) => {
  try {
    const success = categoryService.deleteCategory(req.params.id);
    if (!success) {
      res.status(404).json({ error: 'Category not found' });
      return;
    }
    res.status(204).send();
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

