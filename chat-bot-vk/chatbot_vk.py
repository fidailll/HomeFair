import vk_api
import random
import time
import json
import os
from array import *

# Использовать собственный VK API token для использования чат-бота, данный код был предоставлен для примера.
token = "b114987a91637c4e1f91a51b30a46f1a88c853050341447c258f09422d759094b8c347e5777c93f202b85"
vk = vk_api.VkApi(token=token)
vk._auth_token()

def send_stick(id,number):
    vk.messages.send(user_id=id, stiker_id=number, random_id=1)

def send_photo(id, url):
    vk.messages.send(user_id=id,attachment=url, random_id=1)

def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

def read_file(num, fname):
    f = open(fname, "r")
    for i, line in enumerate(f):
        if i == num:
            return line

def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

#главное меню
k_main = {
    "one_time": False,
    "buttons": [
        [get_button(label="1. Товары", color="primary"), get_button(label="2. Корзина", color="primary")],
        [get_button(label="3. О нас", color="primary"), get_button(label="4. Помощь", color="primary")]
    ]
}
k_main = json.dumps(k_main, ensure_ascii=False).encode('utf-8')
k_main = str(k_main.decode('utf-8'))

#получаем из бд категории товаров и пихаем их сюда в качестве кнопок
#categories
k_categories = {
    "one_time": False,
    "buttons": [
        [get_button(label="?????", color="primary"), get_button(label="?????", color="primary")],
        [get_button(label="В меню", color="default")]
    ]
}
k_categories = json.dumps(k_categories, ensure_ascii=False).encode('utf-8')
k_categories = str(k_categories.decode('utf-8'))

#из списка выбранных товаров берем их и связываем с инфой из бд и пихаем сюда в качестве кнопок для удаления, одна кнопка заказа всего
#selected
k_selected = {
    "one_time": False,
    "buttons": [
        [get_button(label="?????", color="primary"), get_button(label="?????", color="primary")],
        [get_button(label="Заказать", color="positive"), get_button(label="Удалитть все", color="negative")],
        [get_button(label="В меню", color="default")]
    ]
}
k_selected = json.dumps(k_selected, ensure_ascii=False).encode('utf-8')
k_selected = str(k_selected.decode('utf-8'))

#about
k_about = {
    "one_time": False,
    "buttons": [
        [get_button(label="В меню", color="default")]
    ]
}
k_about = json.dumps(k_about, ensure_ascii=False).encode('utf-8')
k_about = str(k_about.decode('utf-8'))
about_us_strings = """
Большая часть продуктов изготавливается под заказ.
Фермеры начинают готовить продукты за день до отправки заказа клиентам.
Именно поэтому мы принимаем заказы заранее и доставляем продукты, максимально свежими.\n
Только самые лучшие продукты могут попасть в наш ассортимент.
Поэтому мы отбираем производителей, которые не используют искусственные добавки для вкуса, цвета и запаха.
В пищу животным не добавляют антибиотики и гормоны роста, а в овощах и фруктах нет пестицидов, 
производители не злоупотребляют азотистыми удобрениями.\n
Мы не просто объединяем фермеров и конечных потребителей, мы также берем на себя две ключевые функции - это контроль качества продуктов и логистику. 
Наша цель - дать возможность людям в больших городах питаться натуральными продуктами,
а жителей сельских территорий обеспечить стабильной работой и понятным будущим.
"""

#support
k_support = {
    "one_time": False,
    "buttons": [
        [get_button(label="?????", color="primary"), get_button(label="?????", color="primary")],
        [get_button(label="?????", color="primary"), get_button(label="В меню", color="default")]
    ]
}
k_support = json.dumps(k_support, ensure_ascii=False).encode('utf-8')
k_support = str(k_support.decode('utf-8'))

# У кнопок может быть один из 4 цветов:
# 1. primary — синяя кнопка, обозначает основное действие. #5181B8
# 2. default — обычная белая кнопка. #FFFFFF
# 3. negative — опасное действие, или отрицательное действие (отклонить, удалить и тд). #E64646
# 4. positive — согласиться, подтвердить. #4BB34B

while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 50, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]

            if body.lower() == "привет":
                vk.method("messages.send", {"peer_id": id, "keyboard": k_main, "message": "Выбери нужный тебе раздел:  ", "random_id": random.randint(1, 2147483647)})

            ####################################################### Товары #########################################################################
            elif body.lower() == "1. товары":
                vk.method("messages.send", {"peer_id": id, "keyboard": k_categories, "message": "Выбери нужный тебе раздел:  ", "random_id": random.randint(1, 2147483647)})

            
            ####################################################### /Товары #########################################################################

            ####################################################### Корзина #########################################################################
            elif body.lower() == "2. корзина":
                vk.method("messages.send", {"peer_id": id, "keyboard": k_selected, "message": "Выбери нужный тебе раздел:  ", "random_id": random.randint(1, 2147483647)})

            
            ####################################################### /Корзина #########################################################################

            ####################################################### О нас #########################################################################
            elif body.lower() == "3. о нас":
                vk.method("messages.send", {"peer_id": id, "keyboard": k_about, "message": about_us_strings, "random_id": random.randint(1, 2147483647)})

            
            ####################################################### /О нас #########################################################################

            ####################################################### Помощь #########################################################################
            elif body.lower() == "4. помощь":
                vk.method("messages.send", {"peer_id": id, "keyboard": k_support, "message": "Выбери нужный тебе раздел:  ", "random_id": random.randint(1, 2147483647)})
 
            elif body.lower() == "??????":
                vk.method("messages.send", {"peer_id": id, "keyboard": k_support, "message": " ", "random_id": random.randint(1, 2147483647)})

            ####################################################### /Помощь #########################################################################

            elif body.lower() == "в меню":
                vk.method("messages.send", {"peer_id": id, "keyboard": k_main, "message": "Выбери нужный тебе раздел:  ", "random_id": random.randint(1, 2147483647)})

            else:
                vk.method("messages.send",
                          {"peer_id": id, "message": "Команда не распознана", "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        time.sleep(1.3)
