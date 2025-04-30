from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from expenses.models import Expense, Category, Budget
from datetime import date


class ExpenseViewsTest(TestCase):
    def setUp(self):
        # Set up a test user, category, budget, and a single expense
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

    # === Home view ===
    def test_home_view_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("expenses-home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/home.html")
        self.assertIn("total_spent", response.context)

    def test_home_view_budget_over(self):
        self.expense.amount = 600  # over budget
        self.expense.save()
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("expenses-home"))
        self.assertIn("🔴 You've gone over budget!", response.context["budget_status"])

    def test_home_view_budget_close(self):
        self.expense.amount = 450  # 90% of budget
        self.expense.save()
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("expenses-home"))
        self.assertIn("🟡 You're close to exceeding your budget!", response.context["budget_status"])

    def test_home_view_unauthenticated(self):
        response = self.client.get(reverse("expenses-home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/home.html")
        self.assertNotIn("total_spent", response.context)

    # === Expense list view ===
    def test_expense_list_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("expense-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/expense_list.html")
        self.assertIn("expenses", response.context)

    # === Expense creation view ===
    def test_expense_create_get(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("expense-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/expense_form.html")

    def test_expense_create_post(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("expense-create"), {
            "category": self.category.id,
            "amount": 75.00,
            "date": date.today().strftime("%Y-%m-%d"),
            "description": "Lunch"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 2)

    # === Expense update view ===
    def test_expense_update_get(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("expense-update", args=[self.expense.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/expense_form.html")

    def test_expense_update_post(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("expense-update", args=[self.expense.id]), {
            "category": self.category.id,
            "amount": 100.00,
            "date": date.today().strftime("%Y-%m-%d"),
            "description": "Updated Dinner"
        })
        self.assertEqual(response.status_code, 302)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.amount, 100.00)

    # === Expense deletion view ===
    def test_expense_delete_get(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("expense-delete", args=[self.expense.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/expense_confirm_delete.html")

    def test_expense_delete_post(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("expense-delete", args=[self.expense.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 0)

    # === Budget view ===
    def test_budget_view_get(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("budget"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/budget_form.html")

    def test_budget_view_post(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("budget"), {
            "amount": 1000
        })
        self.assertEqual(response.status_code, 302)
        self.budget.refresh_from_db()
        self.assertEqual(self.budget.amount, 1000)

    # === Export expenses to CSV ===
    def test_export_expenses_csv(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("export-csv"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("Category,Amount,Date,Description", response.content.decode())
