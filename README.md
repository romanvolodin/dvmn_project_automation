# Автоматизация проектов

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в формате `ПЕРЕМЕННАЯ=значение`.

Доступные переменные:

- `SECRET_KEY` — секретный ключ проекта.
- `DEBUG` — режим отладки. Поставьте `true`, чтобы увидеть отладочную информацию в случае ошибки.
- `ALLOWED_HOSTS` — список доменов/хостов, на которых будет работать сайт. Подробнее в [документации Django](https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts)
- `DB_URL` — путь к базе данных. [Здесь](https://github.com/kennethreitz/dj-database-url#url-schema) можно посмотреть форматы путей для различных баз данных.
- `TRELLO_KEY` — ключ разработчика API Trello, [получить на сайте Trello](https://trello.com/app-key/).
- `TRELLO_TOKEN` — серверный токен Trello для работы со своим аккаунтом , его можно сгенерировать в [разделе Developer API Keys](https://trello.com/app-key/), кликни ссылку "manually generate a Token" в первом абзаце текста.

Пример:

```env
SECRET_KEY=r394nkk!dh&jg!de%ho0e+srarblw$-z3@(k07a1
DEBUG=false
ALLOWED_HOSTS=localhost,127.0.0.1,example.com,www.example.com
DB_URL=sqlite:///db.sqlite3
TRELLO_KEY=ljkndv8*
TRELLO_TOKEN=jnksldjvnkdfbv892e2v0(78(r&5
```