from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import api_router
from app.core.database import engine, Base
from sqlalchemy import text

# Create database tables for MVP (in production, use Alembic)
Base.metadata.create_all(bind=engine)

# Hack for MVP: Ensure 'role' column exists in case DB was created earlier
try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'user' NOT NULL;"))
        conn.commit()
except Exception:
    pass # Column probably already exists

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Pásame. Tú disfruta la comida, nosotros cuadramos la cuenta."}
