class Config:
    #SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Xore4ik55@127.0.0.1:5432/ReadWeldTest"
    #"postgresql://postgres:password@localhost:5433/fastapi"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Xore4ik55@localhost:5433/ReadWeldTest"
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    #SQLALCHEMY_TRACK_MODIFICATIONS = False




class TestConfig(Config):
    SQLALCHEMY_ECHO = True