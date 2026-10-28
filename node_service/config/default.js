const path = require('node:path');

require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

const port = Number(process.env.PORT ?? 3000);

if (!Number.isInteger(port) || port < 1 || port > 65535) {
  throw new Error('PORT must be an integer between 1 and 65535');
}

module.exports = Object.freeze({
  serviceName: process.env.SERVICE_NAME || 'sample-node-service',
  port,
  logLevel: process.env.LOG_LEVEL || 'info',
});