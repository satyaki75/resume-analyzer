from fastapi import FastAPI
from app.routes.analyze import router
from app.db.database import engine, Base
from app.db import models

app = FastAPI()

# include router
app.include_router(router)


# --- DB initialization on startup ---
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)