## Run the API

Install the dependencies and start the development server:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

`GET /health` returns:

```json
{"status": "ok"}
```

`GET /reverse?text=hello` returns:

```json
{"reversed": "olleh"}
```

Interactive API documentation is available at `/docs` while the server is running.

## Authentication microservice

Authentication runs independently from the root API. See [auth_service/README.md](auth_service/README.md) for its setup and endpoints.

## Run tests

```bash
python -m unittest test_main
```