# Generated by Django 5.1.7 on 2025-03-08 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0004_income"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Income",
        ),
    ]
