# Generated by Django 3.0.4 on 2020-03-11 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expenseinfo',
            name='depense',
        ),
    ]
