from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dictalchemy import DictableModel

#SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONN")
pastel_storage_challenge_db_path = 'storage_challenges.sqlite'
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + pastel_storage_challenge_db_path

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(cls=DictableModel)