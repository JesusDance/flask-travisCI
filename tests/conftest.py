import os                                         # #Доступ до змінних середовища
import pytest                                     # #Фреймворк для тестування

from app import create_app                        # #Імпорт фабрики Flask-додатку
from app.db import User, db, Expense
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="module")                   # #Фікстура pytest: створюється один раз на модуль
def test_client():
    os.environ["CONFIG_TYPE"] = "app.config.TestingConfig"
                                                  # #Встановлюємо конфіг для тестового режиму
    flask_app = create_app()                      # #Створюємо Flask-додаток з тестовою конфігурацією

    with flask_app.test_client() as testing_client:
                                                  # #Створюємо тестовий клієнт для HTTP-запитів без запуску сервера
        with flask_app.app_context():             # #Активуємо контекст додатку (необхідний для БД, config, current_app)
            yield testing_client                  # #Передаємо клієнт у тест і чекаємо завершення

@pytest.fixture(scope="module")
def new_user():
    return User(username="Bob_Dilan", password="12345")


@pytest.fixture(scope="module")
def init_database(test_client):
    db.create_all()

    default_user = User(
        username="Mary",
        password=generate_password_hash("some_password", method="pbkdf2")
    )
    second_user = User(
        username="John",
        password=generate_password_hash("some_password", method="pbkdf2")
    )
    db.session.add(default_user)
    db.session.add(second_user)
    db.session.commit()

    expense1 = Expense(title="expense1", amount=5, user_id=default_user.id)
    expense2 = Expense(title="expense2", amount=10, user_id=default_user.id)
    expense3 = Expense(title="expense3", amount=15, user_id=default_user.id)

    db.session.add_all([expense1, expense2, expense3])
    db.session.commit()

    yield

    db.drop_all()


@pytest.fixture(scope="module")
def default_user_token(test_client):
    response = test_client.post(
        "/users/login",
        json={
            "username": "Mary",
            "password": "some_password",
        }
    )
    yield response.json["access_token"]


@pytest.fixture(scope="module")
def second_user_token(test_client):
    response = test_client.post(
        "/users/login",
        json={
            "username": "John",
            "password": "some_password",
        }
    )
    yield response.json["access_token"]
