from flask import Flask, render_template, request, redirect, jsonify, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir, 'expensedatabase.db'))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)  # Adjusted data type to float for amount
    expense_date = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    expense_name = db.Column(db.String(50), nullable=False)


@app.route('/')
def get_all_expenses():
    expenses = Expense.query.all()
    all_total_expenses = []

    if expenses:
        total_expenses = sum(expense.amount for expense in expenses)
        total_business_expenses = sum(
            expense.amount for expense in expenses if expense.category == 'business')
        total_others_expenses = sum(
            expense.amount for expense in expenses if expense.category == 'others')
        total_food_expenses = sum(
            expense.amount for expense in expenses if expense.category == 'food')
        total_entertainment_expenses = sum(
            expense.amount for expense in expenses if expense.category == 'entertainment')
        all_total_expenses = [{"All Expenses": total_expenses}, {"Entertainment": total_entertainment_expenses}, {"Business": total_business_expenses},
                              {"Food": total_food_expenses}, {'Others': total_others_expenses}]

    return render_template("expenses.html", expenses=expenses, all_total_expenses=all_total_expenses)


@app.route('/add_expenses')
def add():
    return render_template("add.html")


@app.route('/add_expenses', methods=['POST'])
def add_expenses():
    try:
        # Retrieve form data
        expense_name = request.form.get("expense_name")
        expense_date = request.form.get("expense_date")
        amount = request.form.get("amount")
        category = request.form.get("category")

        # Create a new Expense object
        new_expense = Expense(expense_name=expense_name,
                              expense_date=expense_date, amount=amount, category=category)

        # Add new_expense to the session and commit to the database
        db.session.add(new_expense)
        db.session.commit()

        return redirect('/')  # Redirect to the home page after adding expense
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/expense/edit/<int:id>', methods=['POST', 'GET'])
def edit_expense(id):
    try:
        # Fetch the expense by its ID
        expense = Expense.query.get(id)

        if request.method == 'GET':
            if expense:
                return render_template("edit.html", expenses=expense)
            else:
                return jsonify({'message': 'Expense not found'}), 404

        elif request.method == 'POST':
            if expense:
                expense.expense_name = request.form.get(
                    'expense_name', expense.expense_name)
                expense.expense_date = request.form.get(
                    'expense_date', expense.expense_date)
                expense.amount = request.form.get('amount', expense.amount)
                expense.category = request.form.get(
                    'category', expense.category)

                # Commit changes to the database
                db.session.commit()
                flash('Expense updated successfully', 'success')

                return redirect('/')
            else:
                return jsonify({'message': 'Expense not found'}), 404

    except Exception as e:
        return jsonify({'message': f"An error occurred: {str(e)}"}), 500


@app.route('/expense/delete/<int:id>')
def delete_expense(id):
    # Fetch the expense by its ID
    expense = Expense.query.get(id)

    # Check if the expense exists
    if expense:
        # Delete the expense from the database
        db.session.delete(expense)
        db.session.commit()
        flash('Expense updated successfully', 'success')
        return redirect('/')

    else:
        return jsonify({'message': 'Expense not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        # Create database tables before running the app
        db.create_all()
    app.run(host='127.0.0.1', port=8088, debug=True)
