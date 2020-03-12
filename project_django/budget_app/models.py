from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
'''
class AccountInfo(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    user_budget = models.IntegerField()
    
    def __str__(self):
        return self.username
'''

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget_name = models.CharField(max_length=100)
    budget_montant = models.DecimalField(max_digits=8, decimal_places=3)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.budget_name)
        super(Budget, self).save(*args, **kwargs)

    def budget_restant(self):
        return self.budget_montant - self.dep_totale()

    def dep_totale(self):
        depenses = ExpenseInfo.objects.filter(budget=self)
        total = 0
        for dep in depenses:
            total += dep.cost 
        return total


class ExpenseInfo(models.Model):
    expense_name = models.CharField(max_length=20)
    cost = models.FloatField()
    date_added = models.DateField()
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE,related_name="expenses_items",null=True)