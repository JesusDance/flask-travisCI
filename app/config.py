from datetime import timedelta


class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///expenses.sqlite3"
    JWT_SECRET_KEY = "jwt_super_secret_key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
