# Node.js Service

This service runs independently from the Python APIs in the repository.

```bash
cd node_service
npm ci
cp .env.example .env
npm run dev
```

The service listens on `http://localhost:3000` by default. `GET /health` reports liveness and uptime; `GET /ready` reports readiness. Request and service logs are emitted as structured JSON.

Run the test suite with `npm test`. Build and run the production container with:

```bash
docker build -t sample-node-service .
docker run --rm -p 3000:3000 sample-node-service
```

Configuration is loaded from environment variables, with optional values in `.env`. See `.env.example` for supported settings.