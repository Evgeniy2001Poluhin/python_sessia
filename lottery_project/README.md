# Lottery API Project

Простое API для управления лотерейными тиражами и билетами, реализованное на FastAPI и SQLite.

## Структура проекта

lottery_project/
├── app/
│   ├── init.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── .env
├── lottery.db
└── requirements.txt


## Инструкция по запуску

1.  **Перейдите в директорию проекта:**
    `cd lottery_project`
2.  **Создайте и активируйте виртуальное окружение:**
    `python3 -m venv venv`
    `source venv/bin/activate`
3.  **Установите зависимости:**
    `pip install -r requirements.txt`
4.  **Запустите приложение:**
    `uvicorn app.main:app --reload`
5.  API будет доступно по адресу: `http://127.0.0.1:8000/docs`

*Для выхода из виртуального окружения используйте `deactivate`.*
