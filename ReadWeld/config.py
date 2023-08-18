import os

#Секретный ключ Flask
FLASK_SECRET_KEY                = os.getenv("FLASK_SECRET_KEY")

# Настройки приложения
APP_HOST                        = os.getenv("APP_HOST")
APP_PORT                        = int(os.getenv("APP_PORT"))
APP_DEBUG                       = bool(os.getenv("APP_DEBUG"))

# Настройки базы данных
DB_URI                          = os.getenv("DB_URI")

#Прочие настройки
PATH_TO_DB_WITH_FILES           = os.getenv("PATH_TO_DB_WITH_FILES")

class Config:
    SQLALCHEMY_DATABASE_URI = DB_URI
    SECRET_KEY = FLASK_SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    SQLALCHEMY_ECHO = True