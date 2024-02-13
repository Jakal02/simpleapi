from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import Engine
from google.cloud.sql.connector import Connector, IPTypes
import os


# helper function to return SQLAlchemy connection pool
def init_connection_pool(connector: Connector) -> Engine:
    # Python Connector database connection function
    def getconn():
        conn = connector.connect(
            os.environ.get("GCP_SQL_INSTANCE_NAME"), # Cloud SQL Instance Connection Name
            "pg8000",
            user=os.environ.get("GCP_SQL_USER"), 
            password=os.environ.get("GCP_PG_PASSWORD"),
            db=os.environ.get("GCP_SQL_DB_NAME"),
            ip_type= IPTypes.PUBLIC,  # IPTypes.PRIVATE for private IP
            enable_iam_auth=True,
        )
        return conn

    SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL , creator=getconn
    )
    return engine

# initialize Cloud SQL Python Connector
connector = Connector()

# create connection pool engine
if os.environ.get("NODE") == 'prod':
    engine = init_connection_pool(connector)
else:
    engine = create_engine(
        "sqlite:///./my_app.db",
        connect_args={
            "check_same_thread": False,
        }
    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

