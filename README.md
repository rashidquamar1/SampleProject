## Run the API

Install the dependencies and start the development server:

```bash
pip install -r requirements.txt
export JWT_SECRET_KEY="$(openssl rand -hex 32)"
uvicorn main:app --reload
```

The API stores user accounts in `users.db` by default. Set `AUTH_DATABASE_PATH` to use another SQLite file.

`GET /health` returns:

```json
{"status": "ok"}
```

`GET /reverse?text=hello` returns:

```json
{"reversed": "olleh"}
```

`POST /auth/register` accepts an email and password as JSON. Passwords must be 8 to 128 characters.

`POST /auth/token` accepts the email as `username` and the password as form data. It returns a bearer access token that expires after 30 minutes.

Send that token as `Authorization: Bearer <token>` to `GET /users/me` to retrieve the authenticated user's email.

Interactive API documentation is available at `/docs` while the server is running.

## Run tests

```bash
python -m unittest
```