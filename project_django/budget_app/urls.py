from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view,name='login'),
    path('add_bud',views.BudgetCreateView.as_view(), name="add"),
    path('app/<slug:slug_budget>',views.index,name='index'),
    path('add_item/<slug:slug_budget>',views.add_item,name='add item'),
    path('logout',views.logout_view,name='logout'),
    path('sign_up',views.sign_up,name="sign up"),
    path('budget_list',views.budget_list,name='budget_list')
    #path('add_budget' ,views.BudgetCreativeView.as_view(), name='add'),
]