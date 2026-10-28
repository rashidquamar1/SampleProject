from fastapi import FastAPI

from auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)


@app.get("/health")
def health_check():
	return {"status": "ok"}


@app.get("/reverse")
def reverse_string(text: str):
	return {"reversed": text[::-1]}