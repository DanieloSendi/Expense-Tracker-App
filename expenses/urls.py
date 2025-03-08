from django.urls import path
from .views import home, expense_list, expense_create, expense_update, expense_delete, budget_view, export_expenses_csv

urlpatterns = [
    path("", home, name="expenses-home"),
    path("expenses/", expense_list, name="expense-list"),
    path("expenses/add/", expense_create, name="expense-create"),
    path("expenses/edit/<int:pk>/", expense_update, name="expense-update"),
    path("expenses/delete/<int:pk>/", expense_delete, name="expense-delete"),
    path("budget/", budget_view, name="budget"),
    path("export/csv/", export_expenses_csv, name="export-csv"),
]
