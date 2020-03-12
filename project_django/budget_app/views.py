from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from .models import ExpenseInfo
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Q
from django.utils.text import slugify
from django.views.generic import CreateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


#Add for the budget view

class BudgetCreateView(LoginRequiredMixin,CreateView):
    login_url='/'
    model = Budget
    template_name = 'budget_app/add-budget.html'
    fields = ('budget_name', 'budget_montant')

    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        return HttpResponseRedirect('/app/'+self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST['budget_name'])

def login_view(request):
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()    
            login(request,user)
            return HttpResponseRedirect("/budget_list")
            
    form=AuthenticationForm()
    return render(request,"registration/login.html", { 'form': form })



@login_required(login_url="/")
def budget_list(request):
    user=request.user
    budgets = Budget.objects.filter(user=user)
    return render(request, 'budget_app/budget-list.html',{'budgets':budgets})

@login_required(login_url="/")
def budget_detail(request, budget_slug):
    budget = get_object_or_404(Budget, slug=budget_slug)
    return render(request,'budget_app/budget-detail.html',{'budget': budget, 'expense_list': budget.expenses.all()})

@login_required(login_url="/")
def index(request,slug_budget):
    budget_ajoute = Budget.objects.get(slug=slug_budget)
    expenses_items = ExpenseInfo.objects.filter(budget=budget_ajoute)
    return render(request,'budget_app/index.html',{'budget':budget_ajoute,'expenses_items':expenses_items})

@login_required(login_url="/")
def add_item(request,slug_budget):
    name = request.POST['expense_name']
    expense_cost = request.POST['cost']
    expense_date = request.POST['expense_date']
    budget = Budget.objects.get(slug=slug_budget)
    ExpenseInfo.objects.create(expense_name=name,cost=expense_cost,date_added=expense_date,budget=budget)
    """budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
    expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
    fig,ax=plt.subplots()
    '''ax.bar(['Expenses','Budget'], [expense_total['expenses'],budget_total['budget']],color=['red','green'])
    ax.set_title('Your total expenses vs. total budget')'''
    plt.savefig('budget_app/static/budget_app/expense.png')"""
    return HttpResponseRedirect('/app/'+slug_budget)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return render(request,'budget_app/budget-list.html')
    form = UserCreationForm()
    return render(request,'budget_app/sign_up.html',{'form':form})
