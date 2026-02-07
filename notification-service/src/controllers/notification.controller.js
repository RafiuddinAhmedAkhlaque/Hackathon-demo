const express = require('express');
const router = express.Router();

router.post('/', (req, res) => {
  res.status(201).json({ message: 'Notification created', data: req.body });
});

router.get('/', (req, res) => {
  res.json({ notifications: [] });
});

router.get('/:id', (req, res) => {
  res.json({ id: req.params.id, message: 'Notification detail' });
});

module.exports = { notificationRouter: router };

