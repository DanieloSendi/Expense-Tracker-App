from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from expenses.models import Expense, Category, Budget
from datetime import date

class ExpenseViewsTest(TestCase):
    def setUp(self):
        """Create a test user, category and sample expenses"""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Food")
        self.budget = Budget.objects.create(user=self.user, amount=500)

        self.expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=50,
            date=date.today(),
            description="Dinner"
        )

    def test_home_view_authenticated(self):
        """Tests the home page for a logged-in user"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("expenses-home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/home.html")
        self.assertIn("total_spent", response.context)
        self.assertIn("budget", response.context)

    def test_home_view_unauthenticated(self):
        """Tests the home page for a non-logged-in user"""
        response = self.client.get(reverse("expenses-home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/home.html")
        self.assertNotIn("total_spent", response.context)  # No data for non-logged-in users

    def test_expense_list_view(self):
        """Tests the display of the list of expenses (must be logged in)"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("expense-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/expense_list.html")
        self.assertIn("expenses", response.context)

    def test_expense_create_view(self):
        """Tests adding a new expense"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("expense-create"), {
            "category": self.category.id,
            "amount": 75.00,
            "date": date.today().strftime("%Y-%m-%d"),
            "description": "Lunch"
        })
        self.assertEqual(response.status_code, 302)  # It should redirect when you add
        self.assertEqual(Expense.objects.count(), 2)  # A new entry should be added
        
    def test_expense_update_view(self):
        """Tests editing an existing expense"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("expense-update", args=[self.expense.id]), {
            "category": self.category.id,
            "amount": 100.00,
            "date": date.today().strftime("%Y-%m-%d"),
            "description": "Updated Dinner"
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.amount, 100.00)

    def test_expense_delete_view(self):
        """Tests the removal of the expense"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("expense-delete", args=[self.expense.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertEqual(Expense.objects.count(), 0)  # Should be removed

    def test_budget_view(self):
        """Tests budget setting"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("budget"), {
            "amount": 1000
        })
        self.assertEqual(response.status_code, 302)
        self.budget.refresh_from_db()
        self.assertEqual(self.budget.amount, 1000)

    def test_export_expenses_csv(self):
        """Tests exporting expenses to CSV file"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("export-csv"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("Category,Amount,Date,Description", response.content.decode())
