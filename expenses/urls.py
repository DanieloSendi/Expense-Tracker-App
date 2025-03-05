from django.urls import path
from .views import home
from .views import expense_list, expense_create, expense_update, expense_delete

urlpatterns = [
    path("", home, name="expenses-home"),
    path("expenses/", expense_list, name="expense-list"),
    path("expenses/add/", expense_create, name="expense-create"),
    path("expenses/edit/<int:pk>/", expense_update, name="expense-update"),
    path("expenses/delete/<int:pk>/", expense_delete, name="expense-delete"),
]