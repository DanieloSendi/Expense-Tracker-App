from django.test import TestCase
from expenses.forms import ExpenseForm, BudgetForm
from expenses.models import Category
from django.contrib.auth.models import User
from datetime import date


class ExpenseFormTest(TestCase):
    def setUp(self):
        Category.objects.all().delete()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Groceries")

    def test_valid_expense_form(self):
        form_data = {
            "category": self.category.id,
            "amount": 150.75,
            "date": date.today().strftime("%Y-%m-%d"),
            "description": "Cinema tickets"
        }
        form = ExpenseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_expense_form(self):
        form_data = {
            "category": self.category.id,
            "amount": "",
            "date": "",
            "description": "Test expense"
        }
        form = ExpenseForm(data=form_data)
        self.assertFalse(form.is_valid())


class BudgetFormTest(TestCase):
    def test_valid_budget_form(self):
        form_data = {"amount": 1000.00}
        form = BudgetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_budget_form(self):
        form_data = {"amount": -500}
        form = BudgetForm(data=form_data)
        self.assertFalse(form.is_valid())
