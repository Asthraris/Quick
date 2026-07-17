from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker , declarative_base

from  src.core.config import settings
# 1. Create the engine using the database URL from your Pydantic settings
ENGINE = create_engine(settings.DATABASE_URL , pool_pre_ping= True)

# 2. Create a session factory for database transactions
session_local = sessionmaker(autocommit= False ,autoflush=False , bind= ENGINE )

# 3. Create the Base registry class that your models will inherit from
Base = declarative_base()

def get_db():
    db = session_local()
    try :
        yield db
    finally:
        db.close()