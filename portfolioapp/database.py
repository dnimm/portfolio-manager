from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from portfolioapp.config import database_config

class Base(DeclarativeBase):
    pass


def create_connection_string() -> str:
    
    return (
        f"mysql+pymysql://{database_config['user']}:{database_config['password']}"
        f"@{database_config['host']}:{database_config['port']}/{database_config['database']}"
    )


try:
    engine = create_engine(
        create_connection_string(),
        echo=False
    )
except Exception as e:
    print("Database connection failed:", str(e))


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


def get_session() -> Session:
    return SessionLocal()
