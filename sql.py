import sqlalchemy
from sqlalchemy.orm import sessionmaker


DSN = 'postgresql://postgres:7777777@localhost:5432/bot_en'

engine = sqlalchemy.create_engine(DSN)




Session = sessionmaker(bind=engine)
session = Session()



session.close()


