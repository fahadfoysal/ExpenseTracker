from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),
    path('', views.list_expenses, name='list_expenses'),
    path('set-budget/', views.set_budget, name='set_budget'),
    path('set-budget/<int:category_id>/', views.set_budget, name='update_budget'),
    path('budgets/', views.list_budgets, name='list_budgets'),
    path('budgets/update/<int:budget_id>/', views.update_budget, name='update_budget'),
    path('summary/', views.summary, name='summary'),
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/update/<int:category_id>/', views.update_category, name='update_category'),
]
