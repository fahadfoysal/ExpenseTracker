from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Budget, Category
from .forms import ExpenseForm, BudgetForm, CategoryForm, ExpenseFilterForm
from django.contrib import messages

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_expenses')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

def list_expenses(request):
    form = ExpenseFilterForm(request.GET or None)
    expenses = Expense.objects.all()

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        category = form.cleaned_data.get('category')

        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)
        if category:
            expenses = expenses.filter(category=category)

    return render(request, 'expenses/list_expenses.html', {'expenses': expenses, 'form': form})

def set_budget(request, category_id=None):
    if category_id:
        budget = get_object_or_404(Budget, category_id=category_id)
    else:
        budget = None

    if request.method == 'POST':
        if budget:
            form = BudgetForm(request.POST, instance=budget)
        else:
            form = BudgetForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('list_budgets')
    else:
        form = BudgetForm(instance=budget)

    return render(request, 'expenses/set_budget.html', {'form': form, 'category_id': category_id})

def list_budgets(request):
    budgets = Budget.objects.all()
    return render(request, 'expenses/list_budgets.html', {'budgets': budgets})

def update_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('list_budgets')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'expenses/update_budget.html', {'form': form, 'budget': budget})

def summary(request):
    categories = Category.objects.all()
    summary_data = []

    for category in categories:
        expenses = Expense.objects.filter(category=category)
        total_expense = sum(expense.amount for expense in expenses)
        budget = Budget.objects.filter(category=category).first()
        budget_amount = budget.amount if budget else 0
        exceeded = total_expense > budget_amount
        summary_data.append({
            'category': category.name,
            'total_expense': total_expense,
            'budget': budget_amount,
            'exceeded': exceeded
        })
        if exceeded:
            messages.warning(request, f'Budget exceeded for category: {category.name}')

    return render(request, 'expenses/summary.html', {'summary_data': summary_data})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = CategoryForm()
    return render(request, 'expenses/add_category.html', {'form': form})

def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'expenses/list_categories.html', {'categories': categories})

def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'expenses/add_category.html', {'form': form, 'update': True})
