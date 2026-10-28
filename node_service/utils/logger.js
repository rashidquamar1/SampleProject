const pino = require('pino');

const config = require('../config/default');

module.exports = pino({
  level: config.logLevel,
  base: { service: config.serviceName },
  timestamp: pino.stdTimeFunctions.isoTime,
});