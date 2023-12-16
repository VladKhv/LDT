
# токен для подключения
token_vk = 'токен_vk'

# LLM модель
MODEL_NAME = "IlyaGusev/saiga_mistral_7b"
DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>"
DEFAULT_RESPONSE_TEMPLATE = "<s>bot\n"

# promt чтобы бое помнил предыдущий вопрос
DEFAULT_SYSTEM_PROMPT = '''
<s>system\nТы — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им.</s>
<s>user\n{вопрос_1}</s>
<s>bot\n{ответ_1}</s>
<s>user\n{вопрос_2}</s>
<s>bot\n{ответ_2}</s>
<s>user\n{новый_вопрос}</s>
<s>bot\n
'''
# Праметры подключения к базе PostgreSQL
dbname = 'db_bot'
user = 'db_user'
password = 'password'
host = 'localhost'
host = '127.0.0.1'

# фильтр запрешенныъ слов
words_ban = ['чушпан', 'урод']
