from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:Davilon_123@localhost:5432/Store2"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)