import os
from dotenv import load_dotenv

DOTENV_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".web.env")
if os.path.exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)
else:
    raise FileNotFoundError(f"""
    Cруктура проекта должна быть следующая:
        |-<папка web сервиса>
            |-ReadWeld
            |-run.py
        |-.env
    
    В данном приложении отсутсвует .env файл.
    env файл содержит основные настройки web-приложения
    Обязательные аргументы, входящте в env файл:
    
        #Секретный ключ Flask
        FLASK_SECRET_KEY            = "..."

        # Настройки приложения
        APP_HOST                    = "..."
        APP_PORT                    = "..."
        APP_DEBUG                   = "..."

        # Настройки базы данных
        DATA_BASE_USERNAME          = "..."
        DATA_BASE_PASSWORD          = "..."
        DATA_BASE_HOST              = "..."
        DATA_BASE_PORT              = "..."
        DATA_BASE_NAME              = "..."

        #Прочие настройки
        PATH_TO_DB_WITH_FILES       = "..."

    При запуске, приложение искало env в директории:
        {DOTENV_PATH}
    
    Текщая директория:
        {os.path.abspath(__file__)}
""")

from ReadWeld import app
from ReadWeld.config import APP_HOST, APP_PORT, APP_DEBUG


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
