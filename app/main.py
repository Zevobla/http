from fastapi import FastAPI
import uvicorn
from app.routers import tron
import os

app = FastAPI()
app.include_router(tron.router)
WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "Welcome to the Tron microservice!")

@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint returning a welcome message."""
    return {"message": WELCOME_MESSAGE}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
