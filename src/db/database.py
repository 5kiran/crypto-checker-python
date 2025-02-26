from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


SQLALCHEMY_DATABASE_URL = 'postgresql://crypto:crypto1@localhost:5432/crypto-checker?schema=public'

Engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autoflush=False, bind=Engine)



def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.commit()
        db.close()


Session = get_db_connection()