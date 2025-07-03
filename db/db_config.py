import logging
from config import DATABASE_URL
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

try:
    Base = declarative_base()
    engine = create_engine(DATABASE_URL, isolation_level="READ UNCOMMITTED")
    Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
except Exception as error:
    logger.error(f"Something went wrong while setting up engine & session factory: {error}")
    Session = None

def get_db_session():
    db_session = None
    try:
        db_session = Session() if Session else None
        yield db_session
    except Exception as error:
        logger.error(f"Error within a db session: {error}")
    finally:
        if db_session: db_session.close()