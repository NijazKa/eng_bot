import sqlalchemy as sq

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    tg_id = sq.Column(sq.Integer, nullable=False)
    name = sq.Column(sq.Text)

class BaseWord(Base):
    __tablename__ = 'base_word'

    id = sq.Column(sq.Integer, primary_key=True)
    eng_word = sq.Column(sq.Text, nullable=False)
    translation = sq.Column(sq.Text, nullable=False)
    example_usage = sq.Column(sq.Text, nullable=False)

class UserWord(Base):
    # связь между таблицами пользователя и слов
    pass

class UserCustomWord(Base):
    #таблица пользовательских слов
    pass


def create_tables(engine):
    #Base.metadata.create_all(engine)
    Base.metadata.drop_all(engine)