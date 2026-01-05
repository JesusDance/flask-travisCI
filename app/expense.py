from flask import Blueprint, jsonify, request
from app.db import Expense, db
from app.schemas import expenses_schema, expense_schema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user

bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@bp.route("/", methods=["POST"])
@jwt_required()
def create_expense():
    """
    Створює нову витрату
    ---
    tags:
        - витрати
    procedures:
        - application/json
    parameters:
        - name: Authorization
          in: header
          description: JWT токен
          required: true
        - name: expense
          in: body
          description: Данні витрати
          required: true
          schema:
            $ref: "#/definitions/ExpenseIn"
    responses:
        201:
            description: Створена витрата
            schema:
                $ref: "#/definitions/ExpenseOut"
        401:
            description: Немає доступу
            schema:
                $ref: "#/definitions/Unauthorized"
        422:
            description: Помилка валідації
    """
    json_data = request.json
    try:
        data = expense_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    new_expense = Expense(title=data["title"], amount=data["amount"],
                          user_id=current_user.id)
    db.session.add(new_expense)
    db.session.commit()

    return jsonify(expense_schema.dump(new_expense)), 201


@bp.route("/", methods=["GET"])
@jwt_required()
def get_expenses():
    """
    Повертає список усіх витрат
    ---
    tags:
        - витрати
    procedures:
        - application/json
    parameters:
        - name: Authorization
          in: header
          description: JWT токен
          required: true
    responses:
        200:
            description: Список витрат
            schema:
                type: array
                items:
                    $ref: "#/definitions/ExpenseOut"
    """
    return jsonify(expenses_schema.dump(current_user.expenses)), 200


@bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_expense(id):
    """
        Повертає одну витрату за ідентифікатором
        ---
        tags:
            - витрати
        procedures:
            - application/json
        parameters:
            - name: Authorization
              in: header
              description: JWT токен
              required: true
            - name: id
              in: path
              description: Ідентифікатор витрати
              required: true
              type: number
        responses:
            200:
                description: Знайдена витрата
                schema:
                    $ref: "#/definitions/ExpenseOut"
            401:
                description: Немає доступу
                schema:
                    $ref: "#/definitions/Unauthorized
            404:
                description: Не знайдено витрату за ідентифікатором
                schema:
                    $ref: "#/definitions/NotFound"
        """
    #expense = db.get_or_404(Expense, id)
    expense = Expense.query.filter_by(id=id, is_deleted=False).first_or_404()
    if expense.user_id != current_user.id:
        return jsonify(error="У вас немає доступу до цієї витрати"), 401

    return jsonify(expense_schema.dump(expense))


@bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_expense(id):
    """
    Оновлює дані витрати за ідентифікатором
    ---
    tags:
        - оновлює витрату
    procedures:
        - application/json
    parameters:
        - name: Authorization
          in: header
          description: JWT токен
          required: true
        - name: id
          in: path
          description: Ідентифікатор витрати
          required: true
          type: integer
        - name: expense
          in: body
          description: Дані для оновлення витрати
          required: true
          schema:
            $ref: "#/definitions/ExpenseIn"
    responses:
        200:
            description: Оновлена витрата
            schema:
              $ref: "#/definitions/ExpenseOut"
        401:
            description: Немає доступу
            schema:
                $ref: "#/definitions/Unauthorized"
        422:
            description: Помилка валідації
    """
    expense = db.get_or_404(Expense, id)

    if expense.user_id != current_user.id:
        return jsonify(error="У вас немає доступу до цієї витрати"), 401

    json_data = request.json
    try:
        data = expense_schema.load(json_data, partial=True)
    except ValidationError as err:
        return err.messages, 422

    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)

    db.session.commit()

    return jsonify(expense_schema.dump(expense))


@bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_expense(id):
    """
    Видалити витрату (soft delete)
    ---
    tags:
        - видалення
    parameters:
        - name: id
          in: path
          required: true
          type: integer
    responses:
          204:
            description: Успішно видалено
    """
    expense = db.get_or_404(Expense, id)
    expense.is_deleted = True

    if expense.user_id != current_user.id:
        return jsonify(error="У вас немає доступу до цієї витрати"), 401

    #db.session.delete(expense)
    db.session.commit()

    return "", 204