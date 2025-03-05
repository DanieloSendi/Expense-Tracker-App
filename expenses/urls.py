from django.urls import path
from .views import home
from .views import expense_list, expense_create, expense_update, expense_delete

urlpatterns = [
    path("", home, name="expenses-home"),
    path("", expense_list, name="expense-list"),
    path("add/", expense_create, name="expense-create"),
    path("edit/<int:pk>/", expense_update, name="expense-update"),
    path("delete/<int:pk>/", expense_delete, name="expense-delete"),
]