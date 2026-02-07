import { Router, Request, Response } from 'express';
import { PricingService } from '../services/pricing.service';
import { ProductRepository } from '../repositories/product.repository';

const productRepo = new ProductRepository();
const pricingService = new PricingService(productRepo);

export const pricingRouter = Router();

pricingRouter.post('/rules', (req: Request, res: Response) => {
  try {
    const rule = pricingService.createRule(req.body);
    res.status(201).json(rule);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

pricingRouter.get('/rules', (_req: Request, res: Response) => {
  const rules = pricingService.getActiveRules();
  res.json(rules);
});

pricingRouter.get('/rules/:id', (req: Request, res: Response) => {
  const rule = pricingService.getRule(req.params.id);
  if (!rule) {
    res.status(404).json({ error: 'Price rule not found' });
    return;
  }
  res.json(rule);
});

pricingRouter.put('/rules/:id', (req: Request, res: Response) => {
  const rule = pricingService.updateRule(req.params.id, req.body);
  if (!rule) {
    res.status(404).json({ error: 'Price rule not found' });
    return;
  }
  res.json(rule);
});

pricingRouter.delete('/rules/:id', (req: Request, res: Response) => {
  const success = pricingService.deleteRule(req.params.id);
  if (!success) {
    res.status(404).json({ error: 'Price rule not found' });
    return;
  }
  res.status(204).send();
});

pricingRouter.get('/calculate/:productId', (req: Request, res: Response) => {
  try {
    const quantity = parseInt(req.query.quantity as string) || 1;
    const result = pricingService.calculatePrice(req.params.productId, quantity);
    res.json(result);
  } catch (error: any) {
    res.status(404).json({ error: error.message });
  }
});

