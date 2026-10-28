const express = require('express');

const config = require('../../config/default');

const router = express.Router();

router.get('/health', (request, response) => {
  response.json({
    status: 'ok',
    service: config.serviceName,
    uptimeSeconds: Math.floor(process.uptime()),
  });
});

router.get('/ready', (request, response) => {
  response.json({ status: 'ready' });
});

module.exports = router;