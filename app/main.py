from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import client
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth_router import router as authorized_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.connect_db()
    yield
    await client.disconnect_db()

app = FastAPI(lifespan=lifespan)  # Remove 'strict_slashes'

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include API routers
app.include_router(authorized_router)

# Healthcheck route
@app.get("/", status_code=200, include_in_schema=False)
async def healthcheck():
    return {"status": "App is online"}
