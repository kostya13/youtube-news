Скрипты для получения новостей.

После скачивания переименовать `config-example.py` в `config.py`.

В файле `config.py` в переменную `TELEGRAM_TOKEN` записать правильный токен
для бота, который получен у BotFather. 

Подключиться в телеграмме к своему боту и отправить ему любое сообщение.
После этого запустить скрипт `get_chat_id.py`. Полученный идентификатор чата записать в `config.py`
в переменную `CHAT_ID`.

Получить ключ от Google, зайти на
https://console.developers.google.com/
Раздел "Credentials".
Занести его в переменную `GOOGLE_API_KEY`.

Так же определить идентификатор своего канала.
https://www.youtube.com/account
В разделе "Мой канал" можно получить ссылку на канал
https://www.youtube.com/channel/<здесь много букв и цифр>
Взять идентификатор который идет после последнего слеша.
Записать его в `MYCHANNEL_ID`.