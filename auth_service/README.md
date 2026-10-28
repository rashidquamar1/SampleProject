# Authentication Service

This service runs independently from the root SampleProject API.

From the SampleProject root, create a dedicated environment, install this service's dependencies, and start it:

```bash
python -m venv auth_service/.venv
source auth_service/.venv/bin/activate
pip install -r auth_service/requirements.txt
export JWT_SECRET_KEY="$(openssl rand -hex 32)"
export AUTH_DATABASE_PATH="$PWD/auth_service/users.db"
uvicorn auth_service.main:app --reload --port 8001
```

The service stores accounts in SQLite. Its endpoints and interactive API docs are available at `http://127.0.0.1:8001` and `/docs`.

- `POST /auth/register`: create an account with an email and an 8- to 128-character password.
- `POST /auth/token`: exchange form fields `username` (email) and `password` for a 30-minute bearer token.
- `GET /users/me`: return the authenticated user's email. Send the token as `Authorization: Bearer <token>`.

Run the authentication tests from the SampleProject root with the service environment activated:

```bash
python -m unittest auth_service.test_auth
```