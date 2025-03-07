from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Expense, Budget
from django.shortcuts import get_object_or_404, redirect
from .forms import ExpenseForm, BudgetForm
from django.db import models


@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user)
    budget = Budget.objects.filter(user=request.user).first()
    total_spent = expenses.aggregate(models.Sum("amount"))["amount__sum"] or 0

    budget_status = None
    if budget:
        percent_used = (total_spent / budget.amount) * 100 if budget.amount > 0 else 0
        if percent_used > 100:
            budget_status = "🔴 You've gone over budget!"
        elif percent_used > 80:
            budget_status = "🟡 You're close to exceeding your budget!"
        else:
            budget_status = f"🟢 Used {percent_used:.2f}% of the budget."
    return render(request, "expenses/home.html", {"expenses": expenses, "budget_status": budget_status})

# Takes all the expenses of a logged-in user and sorts them descending by date.
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    return render(request, "expenses/expense_list.html", {"expenses": expenses})

# Creates a new expense and assigns it to the currently logged-in user.
@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("expense-list")
    else:
        form = ExpenseForm()
    return render(request, "expenses/expense_form.html", {"form": form})

# It retrieves the expense from the database and allows you to edit it.
@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expense-list")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "expenses/expense_form.html", {"form": form})

# Deletes the expense only if the user confirms it.
@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect("expense-list")
    return render(request, "expenses/expense_confirm_delete.html", {"expense": expense})


@login_required
def budget_view(request):
    budget, created = Budget.objects.get_or_create(user=request.user, defaults={"amount": 0.00})
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect("expenses-home")
    else:
        form = BudgetForm(instance=budget)
    return render(request, "expenses/budget_form.html", {"form": form})
