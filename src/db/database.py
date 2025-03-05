from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


from src.db.models import user_model
from src.db.models import wallet_model
from src.db.models import project_model
from src.db.models import mission_model
from src.db.models import post_model
from src.db.models import comment_model
from src.db.models import joined_mission_model

SQLALCHEMY_DATABASE_URL = "postgresql://crypto:crypto1@localhost:5432/crypto-checker"

engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    connect_args={"options": "-c search_path=public"},
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db() -> Session:
    session = SessionLocal()
    try:
        yield session
    except:
        session.rollback()
    finally:
        session.close()
