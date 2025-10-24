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
def target_translate(id = 1500) -> list:
    # target_list = []
    # for target_trans in session.query(sql.Word).filter(sql.Word.id == id).all():
    #     target_list.append(target_trans.eng_word)
    #     target_list.append(target_trans.translation)
    #     target_list.append(target_trans.id)
    target_list = session.query(sql.Word).filter(sql.Word.id == id).all()
    return target_list

def new_word(tg_id: int, word_id: int) -> None:
    for user_id in session.query(sql.User).filter(sql.User.tg_id == tg_id).all():

        try:
            user_word = sql.UserWord(user_id=user_id.id, word_id=word_id)
            session.add(user_word)
            session.commit()
        except:
            pass



def new_user(uid: int):
    if session.query(sql.User).filter(sql.User.tg_id == uid).all():
        print('пользователь есть')
    else:
        print('нет пользователя')