from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database = "postgresql+psycopg2://postgres:contactspassword@localhost:5432/postgres"
engine = create_engine(database)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()