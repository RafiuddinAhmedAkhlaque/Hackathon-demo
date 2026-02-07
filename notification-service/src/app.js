const express = require('express');
const { notificationRouter } = require('./controllers/notification.controller');
const { templateRouter } = require('./controllers/template.controller');

function createApp() {
  const app = express();
  app.use(express.json());

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

