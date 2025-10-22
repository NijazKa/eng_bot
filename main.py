import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables

DSN = 'postgresql://postgres:7777777@localhost:5432/bot_en'

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()



session.close()