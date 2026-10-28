const express = require('express');
const pinoHttp = require('pino-http');

const healthRoutes = require('./routes/health');
const logger = require('../utils/logger');

const app = express();

app.disable('x-powered-by');
app.use(
  pinoHttp({
    logger,
    serializers: {
      req(request) {
        return {
          id: request.id,
          method: request.method,
          url: request.url,
          remoteAddress: request.remoteAddress,
        };
      },
    },
    customLogLevel(request, response, error) {
      if (error || response.statusCode >= 500) return 'error';
      if (response.statusCode >= 400) return 'warn';
      return 'info';
    },
  }),
);
app.use(healthRoutes);
app.use((error, request, response, next) => {
  logger.error({ err: error }, 'Unhandled request error');
  response.status(500).json({ error: 'Internal Server Error' });
});

module.exports = app;