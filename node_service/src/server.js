const app = require('./app');
const config = require('../config/default');
const logger = require('../utils/logger');

const server = app.listen(config.port, () => {
  logger.info({ port: config.port }, 'Service listening');
});

server.on('error', (error) => {
  logger.error({ err: error }, 'Service failed to start');
  process.exitCode = 1;
});

function shutdown(signal) {
  logger.info({ signal }, 'Service shutting down');
  server.close((error) => {
    if (error) {
      logger.error({ err: error }, 'Error while shutting down');
      process.exitCode = 1;
    }
  });
}

process.once('SIGINT', () => shutdown('SIGINT'));
process.once('SIGTERM', () => shutdown('SIGTERM'));