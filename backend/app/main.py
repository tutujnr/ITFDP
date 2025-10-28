from fastapi import FastAPI
from .database import engine
from . import models
from .routes import router
from fastapi.staticfiles import StaticFiles

# create tables (for MVP; in production use Alembic)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tea Farmers Platform (MVP)")

app.include_router(router)

# Serve uploads for demo purposes
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
