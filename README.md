# LDT
"Умный цифровой помощник Главы региона"

Решение написано на языке Python, используется модель "Сайга Мистраль", база PostgreSQL, API VK
В качестве основного компонента, была использована российская бесплатная LLM модель "Сайга Мистраль".
Характеристики LLM модели "Сайга Мистраль":
1. Использует Grouped-query attention (GQA) для более быстрой обработки.
2. Использует Sliding Window Attention (SWA) для обработки длинных последовательностей токенов с меньшими затратами.
3. Скорость генерации ответов около 70 символов в секунду, что крайне быстро.


Для решения задачи были написаны следующие программные модули:
1. Экспорт теста с pdf файлов, с разбиением на абзацы, получения эмбедингов абзацев и сохранение результатов в базе PostgreSQL.
2. Экспорт теста из текстовых файлов, с разбиением на абзацы, получения эмбедингов абзацев и сохранение результатов в базе PostgreSQL.
3. Создан и подключен в модели, с помощью API VK бот (ссылка https://vk.com/club223781373).

Описание решения.
1. При первом использовании (сначала нужно установить необходимые библиотеки командой "python -m pip install -r requirements.txt"):
- создается база PostgreSQL, с необходимыми таблицами.
- запускаются модули экспорта (из тестовых файлов), которые наполняют базу информацией и эмбедингами.
- по каждому тексту, модель "Сайга Мистраль", генерерирует 5 впросов и ответов на них. Этим мы достигаем наполнение базы вопросами и ответами на них.
- запускается модуль модели "Сайга Мистраль".
- запускается API VK.
Все - решение готово к работе.

2. Основная работа - ответы на вопросы.
- При получении вопроса от пользователя, происходит корректировка орфографии, анализ на не нормативную лексику.
- Далее вопрос переводится в эмбединги.
- По эмбедингу вопроса и эмбедингу текста ищется наиболее релевантная часть текста в базе PostgreSQL.
- Модель "Сайга Мистраль" ищет ответ на вопрос в ревалентном тексте (технология RAG (Retrieval-Augmented Generation)).
- Полученный ответ через API VK отсылается пользователю.
- Так же, все заданные вопросы и ответы на них, кешируются в PostgreSQL, что намного снижает накладные расходы и время ответа, при получении вопросов, на которые уже был дан ответ. 


Куда развиваться в будущем - отказаться от технологии RAG, и дообучить модель на собственных данных (для обучения на новых данных нужно несколько суток непрерывной работы).
Сохранять id пользователя, чтобы "помнить историю" - при каждом новом подключении пользователя, который уже задавал вопросы, из базы PostgreSQL получать предыдущий вопрос и ответ на него.

Порядок запуска.
1. Выполняем код "Подготовка к первому запуску.ipynb" - при этом создается необходимая база, происходит ее заполнение текстом из документов и генерируются вопросы по тексту.
2. Запускаем "start_bot.py" - бот готов к работе.
3. Ссылка на бота - https://vk.com/club223781373
