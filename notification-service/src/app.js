const express = require('express');
const { notificationRouter } = require('./controllers/notification.controller');
const { templateRouter } = require('./controllers/template.controller');

// JSON logging middleware
const jsonLoggingMiddleware = (req, res, next) => {
  const startTime = Date.now();
  
  res.on('finish', () => {
    const duration_ms = Date.now() - startTime;
    
    const log_data = {
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration_ms: duration_ms,
      timestamp: new Date().toISOString()
    };
    
    console.log(JSON.stringify(log_data));
  });
  
  next();
};

function createApp() {
  const app = express();
  app.use(express.json());

  // Add JSON logging middleware
  app.use(jsonLoggingMiddleware);

  app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'notification-service' });
  });

  app.use('/notifications', notificationRouter);
  app.use('/templates', templateRouter);

  return app;
}

if (require.main === module) {
  const app = createApp();
  const PORT = process.env.PORT || 8006;
  app.listen(PORT, () => {
    console.log(`Notification Service running on port ${PORT}`);
  });
}

module.exports = { createApp };

