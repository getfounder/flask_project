import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from data.users import User
from data import db_session
import uuid
import hashlib


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


RANDOM_ID_LIMIT = 2 ** 64
c = 0
db_session.global_init("db/data.db")
def main():
    global c
    Token = '226e3aec9be92093f69277c1c90a45563ce79461838eb3aa8ef1a69b3e01818d20bdcdb84e7308811bcef'
    vk_session = vk_api.VkApi(token=Token)

    longpoll = VkBotLongPoll(vk_session, 203399900)

    for event in longpoll.listen():
        print(event)
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            print(event.obj.message['text'].lower())
            if c == 0 or 'привет' in event.obj.message['text'].lower() or 'хай' in event.obj.message['text'].lower():
                text = 'Привет! Ты уже был на нашем сайте? Ты зарегестрировался?' \
                       ' А давай проверим? Введи электронную почту и пароль через ПРОБЕЛ, и я тебе отвечу.'
                c = 1
            else:
                c = 0
                s1 = event.obj.message['text'].lower().split()
                if len(s1) == 2:
                    db_sess = db_session.create_session()
                    user = db_sess.query(User).filter(User.email == s1[0]).first()
                    if user and check_password(user.password, s1[1]):
                        text = 'Молодец! Ты зарегестрирован! А как давно ты был на нашем сайте? Там переодически появляются новые акции и предложения.'
                    else:
                        text = 'Вы не зарегестрированы((((( Обязательно сделайте это, ведь на нашем сайте' \
                               ' переодически появляются интересные предложения и у нас одна из лучших техник в городе!!!!'
                else:
                    text = 'Вы не зарегестрированы((((( Обязательно сделайте это, ведь на нашем сайте' \
                           ' переодически появляются интересные предложения и у нас одна из лучших техник в городе!!!!'
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             random_id=random.randint(0, RANDOM_ID_LIMIT))


if __name__ == '__main__':
    main()
