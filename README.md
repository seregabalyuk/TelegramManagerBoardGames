# Инструкция по установке

## Настраиваем Python
Настраиваем окружение:
```bash
python3 -m venv penv # создаём окружение
source penv/bin/activate # активируем окружение
pip install -r src/requirements.txt # устанавливаем нужные библиотки
```
Для выхода из окружения:
```bash
deactivate 
```
## Настраиваем PostgreSQL
Для начала, установите PostgreSQL
```bash
# хз что тут делать
```

Потом:
```bash
sudo -u postgres psql # заходим в psql
```
И там набираем
```sql
CREATE USER board_game_bot WITH PASSWORD 'bot'; -- добовляем пользователя
CREATE DATABASE board_game_database OWNER board_game_bot; -- создаем базу данных
GRANT ALL PRIVILEGES ON DATABASE board_game_database TO board_game_bot; -- даем все привилегии
\c board_game_database -- переключаемся на нашу базу данных
\i src/database/create.sql -- создаем таблицы
```
## Настраеваем Бота в Тг
[Сайт с инструкцией для регистрации бота в тг](https://ibot.by/info/base/token/)

[Наш бот](https://t.me/BoardGameManagerBot)
