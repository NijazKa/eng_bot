import random
import sql
from sql import session



# функция получения рандомного слова (нужно получить как то актуальные id слов, пока цифрами)
def random_word() -> list:
    n = 0
    rand_word_list = []
    while n < 4:
        n += 1
        for rand_word in session.query(sql.Word).filter(sql.Word.id == random.randint(1027, 2006)).all():
            rand_word_list.append(rand_word.eng_word)
    return rand_word_list

# возвращает список рус\анг слова по id
def target_translate(id = 1500):
    target_list = session.query(sql.Word).filter(sql.Word.id == id).first()
    return target_list

def new_word(tg_id: int, word_id: int) -> None:
    # Находим пользователя
    user = session.query(sql.User).filter(sql.User.tg_id == tg_id).first()
    if not user:
        return
    # Проверяем, есть ли уже такое слово у пользователя
    existing_word = session.query(sql.UserWord).filter(
            sql.UserWord.word_id == word_id
            ).first()

    if existing_word:
         return

    # Добавляем новое слово
    user_word = sql.UserWord(user_id=user.id, word_id=word_id, wrong_attempts=0)
    session.add(user_word)
    session.commit()


def new_user(uid: int):
    if session.query(sql.User).filter(sql.User.tg_id == uid).all():
        print('пользователь есть')
    else:
        print('нет пользователя')

