import sqlalchemy
from sqlalchemy.orm import sessionmaker
import requests
import csv
from models import Word

DSN = 'postgresql://postgres:7777777@localhost:5432/bot_en'

engine = sqlalchemy.create_engine(DSN)


Session = sessionmaker(bind=engine)
session = Session()



with open('words.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        description = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{row[0]}')
        try:
            desc_text = description.json()[0]['meanings'][-1]['definitions'][0]['example']
        except:
            try:
                desc_text = description.json()[0]['meanings'][0]['definitions'][0]['example']
            except:
                try:
                    desc_text = description.json()[0]['meanings'][1]['definitions'][0]['example']
                except:
                    try:
                        desc_text = description.json()[0]['meanings'][2]['definitions'][0]['example']
                    except:
                        desc_text = 'нет примеров'

        #print(desc_text)
        word = Word(eng_word=row[0], translation=row[1], example_usage=desc_text)
        session.add(word)
        session.commit()
