

from ReadWeld import app




import os

APP_HOST    = os.getenv("APP_HOST")
APP_PORT    = int(os.getenv("APP_PORT"))
APP_DEBUG   = bool(os.getenv("APP_DEBUG"))


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
