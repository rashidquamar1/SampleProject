const request = require('supertest');

const app = require('../src/app');

describe('health endpoints', () => {
  test('GET /health reports service health and uptime', async () => {
    const response = await request(app).get('/health');

    expect(response.status).toBe(200);
    expect(response.body).toEqual({
      status: 'ok',
      service: 'sample-node-service',
      uptimeSeconds: expect.any(Number),
    });
    expect(response.headers).not.toHaveProperty('x-powered-by');
  });

  test('GET /ready reports readiness', async () => {
    const response = await request(app).get('/ready');

    expect(response.status).toBe(200);
    expect(response.body).toEqual({ status: 'ready' });
  });
});