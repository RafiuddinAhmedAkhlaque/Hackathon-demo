import express from 'express';
import { productRouter } from './controllers/product.controller';
import { categoryRouter } from './controllers/category.controller';
import { pricingRouter } from './controllers/pricing.controller';
import { errorHandler } from './middleware/error-handler.middleware';

export function createApp(): express.Application {
  const app = express();

  app.use(express.json());

  // Health check
  app.get('/health', (_req, res) => {
    res.json({ status: 'healthy', service: 'product-service' });
  });

  // Routes
  app.use('/products', productRouter);
  app.use('/categories', categoryRouter);
  app.use('/pricing', pricingRouter);

  // Error handler
  app.use(errorHandler);

  return app;
}

if (require.main === module) {
  const app = createApp();
  const PORT = process.env.PORT || 8002;
  app.listen(PORT, () => {
    console.log(`Product Service running on port ${PORT}`);
  });
}

