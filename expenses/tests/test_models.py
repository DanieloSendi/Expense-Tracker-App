from django.test import TestCase
from django.contrib.auth.models import User
from expenses.models import Category, Expense, Budget
from datetime import date

class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.all().delete()
        
    def test_category_creation(self):
        category = Category.objects.create(name="Food")
        self.assertEqual(str(category), "Food")
        self.assertEqual(Category.objects.count(), 1)

class ExpenseModelTest(TestCase):
    def setUp(self):
        Category.objects.all().delete()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Groceries")

    def test_expense_creation(self):
        expense = Expense.objects.create(
            user=self.user, category=self.category, amount=100.50, date=date.today(), description="Weekly groceries"
        )
        self.assertEqual(expense.amount, 100.50)
        self.assertEqual(expense.user.username, "testuser")
        self.assertEqual(expense.category.name, "Groceries")
        self.assertEqual(str(expense), f"{expense.amount:.2f} - {self.category} ({expense.date})")


class BudgetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_budget_creation(self):
        budget = Budget.objects.create(user=self.user, amount=500)
        self.assertEqual(budget.amount, 500)
        self.assertEqual(budget.user.username, "testuser")
        self.assertEqual(str(budget), "Budget testuser: 500")
