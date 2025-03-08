from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.amount} - {self.category} ({self.date})"


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == "expenses":
        default_categories = ["Groceries", "Transport", "Healthcare", "Entertainment", "Travel", "Education", "Housing utilities"]
        for category_name in default_categories:
            Category.objects.get_or_create(name=category_name)
            

# Storage of the user's budget
class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One budget per user
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # The amount of monthly budget

    def __str__(self):
        return f"Budget {self.user.username}: {self.amount}"
    