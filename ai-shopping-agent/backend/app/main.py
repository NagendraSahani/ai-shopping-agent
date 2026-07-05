from fastapi import FastAPI

app = FastAPI(
    title="AI Shopping Agent",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Welcome to AI Shopping Agent 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }