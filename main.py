
from pyaspeller import YandexSpeller
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config_telebot.py import *
import joblib
from sentence_transformers import SentenceTransformer
import torch
import json
from sentence_transformers import SentenceTransformer
import random
import numpy as np

# для исправления ошибок
speller = YandexSpeller()

# подключаемся к базе
connection = psycopg2.connect(
    dbname = dbname,
    user = user, 
    password = password, 
    host = host
)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()

# выводим версию базы
sql = 'SELECT version();'
cursor.execute(sql)
records = cursor.fetchall()
print(records)

# фиксируем генератор случайных чисел
seed = 0
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)

# модель для получения эмбендингов
embeddings_model = SentenceTransformer(
    'intfloat/multilingual-e5-large',
    device = 'cpu'
)
def get_embedding(sentence):    
    embeddings = embeddings_model.encode(sentence)
    return embeddings

# основная функция для получения ответов
def get_answer(question):
    
    question = speller.spelled(question)    
    question = question.replace('\xa0', '')
    question = question.replace('\n', ' ')
    question = question.replace('.', '. ')
    question = question.replace('...', '... ')
    question = question.replace(',', ', ')
    question = question.replace('!', '! ')
    question = question.replace('  ', ' ')
    question = question.replace('   ', ' ')
    question = question.replace('    ', ' ')
    
    # если среди слов есть запрещенное - заканчиваем беседу
    for w in words_ban:
        if w in question.lower():
            return 'Я не могу говорить на эту тему.'
    
    
    # получаем эмбендинг вопроса
    embedding = get_embedding(question)
    query_embedding = json.dumps(embedding.tolist())
    
    # ищем ближайщий эмбендинг к эмбендингу вопроса
    cursor.execute(
    """SELECT question, answer, 1 - (emb <=> %s) AS cosine_similarity
            FROM embedding
            ORDER BY cosine_similarity DESC LIMIT 3""",
        (query_embedding,)
    )
    records = cursor.fetchall()    
    
    # 
    try:
        print('cosine_similarity', records[0][2])
    except:
        records = [[0,0,0]]        
    
    # если вопрос уже был - берем ответ из базы
    if records[0][2] > 0.975:
        answer = records[0][1]        
        print('Ответ из базы:')
        return answer
    
    # если похожего вопроса не было ищем ближайший текст по эмбендингу вопроса
    cursor.execute(
        """SELECT text_doc, 1 - (emb_theme <=> %s) AS cosine_similarity
                FROM documents
                ORDER BY cosine_similarity DESC LIMIT 3""",
            (query_embedding,)
    )
    records2 = cursor.fetchall()
    text_doc = records2[0][0]
    cosine_similarity2 = records2[0][1]    
    
    print('cosine_similarity', records2[0][1])
    
    # отвечаем на вопрос по тесту
    
    promnt = '<s>system\nОтветь кратко на вопрос. Не более 100 слов.</s>'    
    answer = model_qa.predict_answer(promnt + text_doc + question)
    answer = answer.replace('  ', ' ').replace('   ', ' ').replace('    ', ' ')    
    
    return answer
