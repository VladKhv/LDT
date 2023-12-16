
from model_gpu import *
import random
from config_telebot import *
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import time
from commander.commander import Commander
import torch
import gc
import time

def write_msg(user_id, message):
    vk.method(
        'messages.send', {
            'user_id': user_id, 
            'message': message, 
            'random_id': random.randint(0, 2048)
        }
    )

# Авторизуемся как сообщество
vk = vk_api.VkApi(token = token_vk)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Commander
commander = Commander()

print("Бот запущен")
# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня(то есть бота)
        if event.to_me:
            start_time = time.time()

            # Сообщение от пользователя
            question = event.text
            
            answer = get_answer(question)

            #Логика ответа
            write_msg(event.user_id, answer)
            
            print(question, '->')
            print(answer)
            end_time = time.time()
            total_time = (end_time - start_time)
            print(f'время на ответ: {int(total_time)} сек', '\n')
            
            torch.cuda.empty_cache()
            gc.collect()
