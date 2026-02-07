const express = require('express');
const router = express.Router();

router.post('/', (req, res) => {
  res.status(201).json({ message: 'Template created', data: req.body });
});

router.get('/', (req, res) => {
  res.json({ templates: [] });
});

router.get('/:id', (req, res) => {
  res.json({ id: req.params.id, message: 'Template detail' });
});

module.exports = { templateRouter: router };

