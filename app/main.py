from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api import router as api_router


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # You can specify specific headers if needed
)

app.include_router(api_router, prefix="/api")
