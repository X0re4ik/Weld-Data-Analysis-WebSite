import os

#Секретный ключ Flask
FLASK_SECRET_KEY                = os.getenv("FLASK_SECRET_KEY")

# Настройки приложения
APP_HOST                        = os.getenv("APP_HOST")
APP_PORT                        = int(os.getenv("APP_PORT"))
APP_DEBUG                       = bool(os.getenv("APP_DEBUG"))

# Настройки базы данных
DATA_BASE_TITLE                 = os.getenv("DATA_BASE_TITLE")
DATA_BASE_USERNAME              = os.getenv("DATA_BASE_USERNAME")
DATA_BASE_PASSWORD              = os.getenv("DATA_BASE_PASSWORD")
DATA_BASE_HOST                  = os.getenv("DATA_BASE_HOST")
DATA_BASE_PORT                  = os.getenv("DATA_BASE_PORT")
DATA_BASE_NAME                  = os.getenv("DATA_BASE_NAME")

#Прочие настройки
PATH_TO_DB_WITH_FILES           = os.getenv("PATH_TO_DB_WITH_FILES")


class Config:
    SQLALCHEMY_DATABASE_URI = f"{DATA_BASE_TITLE}://{DATA_BASE_USERNAME}:{DATA_BASE_PASSWORD}@{DATA_BASE_HOST}:{DATA_BASE_PORT}/{DATA_BASE_NAME}"
    SECRET_KEY = FLASK_SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    SQLALCHEMY_ECHO = True