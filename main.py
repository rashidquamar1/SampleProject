from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check():
	return {"status": "ok"}


@app.get("/reverse")
def reverse_string(text: str):
	return {"reversed": text[::-1]}