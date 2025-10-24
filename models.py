import sqlalchemy as sq
from sqlalchemy import ForeignKey

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    tg_id = sq.Column(sq.Integer, nullable=False, unique=True)
    name = sq.Column(sq.Text, default=None)

    def __str__(self):
        return f'{self.tg_id}, {self.name}'

class Word(Base):
    __tablename__ = 'word'

    id = sq.Column(sq.Integer, primary_key=True)
    eng_word = sq.Column(sq.Text, nullable=False, unique=True)
    translation = sq.Column(sq.Text, nullable=False)
    example_usage = sq.Column(sq.Text, nullable=False)

class UserWord(Base):
    __tablename__ = 'user_word'
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, ForeignKey('user.id', ondelete='CASCADE'))
    word_id = sq.Column(sq.Integer, ForeignKey('word.id', ondelete='CASCADE'))
    is_learned = sq.Column(sq.Boolean, default=False)
    wrong_attempts = sq.Column(sq.Integer)

    user = relationship("User", backref="user_words")
    word = relationship("Word", backref="user_words")


class UserCustomWord(Base):
    __tablename__ = 'custom_word'
    # таблица пользовательских слов
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, ForeignKey('user.id', ondelete='CASCADE'))
    eng_word = sq.Column(sq.Text, nullable=False)
    translation = sq.Column(sq.Text, nullable=False)
    example_usage = sq.Column(sq.Text, nullable=False)
    wrong_attempts = sq.Column(sq.Integer)
    user = relationship(User, backref='customs_words')





def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# create_tables()