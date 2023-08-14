from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.conf.config import settings

database = settings.sqlalchemy_database_url
engine = create_engine(database)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()