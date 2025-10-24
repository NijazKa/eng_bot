import sqlalchemy
from sqlalchemy.orm import sessionmaker
import csv
import requests

from models import create_tables, User, Word, UserWord, UserCustomWord

DSN = 'postgresql://postgres:7777777@localhost:5432/bot_en'

engine = sqlalchemy.create_engine(DSN)

#create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

# u1 = User(tg_id=333, name='nijaz')
# u2 = User(tg_id=444, name='nijaz')
# u1 = User(tg_id=333, name='nijazka')
# session.add(u1)
# session.commit()


# with open('words.csv') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         description = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{row[0]}')
#         try:
#             desc_text = description.json()[0]['meanings'][-1]['definitions'][0]['example']
#         except:
#             try:
#                 desc_text = description.json()[0]['meanings'][0]['definitions'][0]['example']
#             except:
#                 try:
#                     desc_text = description.json()[0]['meanings'][1]['definitions'][0]['example']
#                 except:
#                     try:
#                         desc_text = description.json()[0]['meanings'][2]['definitions'][0]['example']
#                     except:
#                         desc_text = 'нет примеров'
#
#         print(desc_text)
#         word = Word(eng_word=row[0], translation=row[1], example_usage=desc_text)
#         session.add(word)
#         session.commit()
#         #print(row[0], row[1])

session.close()


#  добавить данные в таблицу и закрыть сессию
# session.add_all([],[])
# session.commit()

# достать все данные из таблицы
# session.query(User).all()

# достать определенные данные из таблицы
# session.query(User).filter(User.id > 1).all()
# session.query(User).filter(User.name.like(%nijaz%)).all()

# объединение таблиц
# session.query(User).join(Word.user).all()

# редактировани данных в таблце
#
# session.query(User).filter(User.name == 'nijaz').update({'name': 'lada'})
# session.commit()