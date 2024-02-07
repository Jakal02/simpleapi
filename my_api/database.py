from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DB_URL = "sqlite:///./my_app.db"

engine = create_engine(
    SQLALCHEMY_DB_URL,
    connect_args= {
        "check_same_thread": False,
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

