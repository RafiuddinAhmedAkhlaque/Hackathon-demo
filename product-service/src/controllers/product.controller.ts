import { Router, Request, Response } from 'express';
import { ProductService } from '../services/product.service';
import { ProductRepository } from '../repositories/product.repository';
import { CategoryRepository } from '../repositories/category.repository';

const productRepo = new ProductRepository();
const categoryRepo = new CategoryRepository();
const productService = new ProductService(productRepo, categoryRepo);

export const productRouter = Router();

productRouter.post('/', (req: Request, res: Response) => {
  try {
    const product = productService.createProduct(req.body);
    res.status(201).json(product);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

productRouter.get('/', (req: Request, res: Response) => {
  const skip = parseInt(req.query.skip as string) || 0;
  const limit = parseInt(req.query.limit as string) || 100;
  const products = productService.listProducts(skip, limit);
  res.json(products);
});

productRouter.get('/search', (req: Request, res: Response) => {
  const query = {
    name: req.query.name as string,
    categoryId: req.query.categoryId as string,
    minPrice: req.query.minPrice ? parseFloat(req.query.minPrice as string) : undefined,
    maxPrice: req.query.maxPrice ? parseFloat(req.query.maxPrice as string) : undefined,
    tags: req.query.tags ? (req.query.tags as string).split(',') : undefined,
  };
  const products = productService.searchProducts(query);
  res.json(products);
});

productRouter.get('/:id', (req: Request, res: Response) => {
  const product = productService.getProduct(req.params.id);
  if (!product) {
    res.status(404).json({ error: 'Product not found' });
    return;
  }
  res.json(product);
});

productRouter.put('/:id', (req: Request, res: Response) => {
  try {
    const product = productService.updateProduct(req.params.id, req.body);
    if (!product) {
      res.status(404).json({ error: 'Product not found' });
      return;
    }
    res.json(product);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

productRouter.delete('/:id', (req: Request, res: Response) => {
  const success = productService.deleteProduct(req.params.id);
  if (!success) {
    res.status(404).json({ error: 'Product not found' });
    return;
  }
  res.status(204).send();
});

productRouter.post('/:id/tags', (req: Request, res: Response) => {
  const product = productService.addTags(req.params.id, req.body.tags);
  if (!product) {
    res.status(404).json({ error: 'Product not found' });
    return;
  }
  res.json(product);
});

productRouter.delete('/:id/tags', (req: Request, res: Response) => {
  const product = productService.removeTags(req.params.id, req.body.tags);
  if (!product) {
    res.status(404).json({ error: 'Product not found' });
    return;
  }
  res.json(product);
});

