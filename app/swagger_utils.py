from flask_swagger import swagger


def build_swagger(app):
    swg = swagger(app)
    swg["info"]["title"] = "Додаток контролю витрат"
    swg["info"]["version"] = "0.0.1"
    swg["definitions"] = {
        "Hello": {
            "type": "object",
            "discriminator": "helloType",
            "properties": {"message": {"type": "string"}},
            "example": {"Message": "Привіт, я твій додаток контролю витрат"},
        },
        "UserIn": {
            "type": "object",
            "discriminator": "userInType",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "example": {
                "username": "admin",
                "password": "admin",
            },
        },
        "UserOut": {
            "type": "object",
            "discriminator": "userInType",
            "properties": {
                "id": {"type": "number"},
                "username": {"type": "string"},
            },
            "example": {
                "id": 0,
                "username": "admin",
            },
        },
        "TokenOut": {
            "type": "object",
            "discriminator": "tokenOutType",
            "properties": {
                "access_token": {"type": "string"},
            },
        },
        "Unauthorized": {
            "type": "object",
            "discriminator": "unauthorizedType",
            "properties": {"error": {"type": "string"}},
            "example": {"error": "У вас немає доступу"},
        },
        "ExpenseIn": {
            "type": "object",
            "discriminator": "expenseInType",
            "properties": {
                "title": {"type": "string"},
                "amount": {"type": "number"},
            },
            "example": {
                "title": "Я ваша витрата",
                "amount": 0,
            },
        },
        "ExpenseOut": {
            "type": "object",
            "allOf": [
                {"$ref": "#/definitions/ExpenseIn"},
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"}
                    },
                    "example": {
                        "id": 0,
                    },
                },
            ],
        },
        "NotFound": {
            "type": "object",
            "discriminator": "notFoundType",
            "properties": {"error": {"type": "string"}},
            "example": {"error": "Ми не змогли це знайти :("},
        },
    }
    return swg