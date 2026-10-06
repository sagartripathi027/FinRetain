from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

from django.db.models import Subquery, OuterRef
from predictions.models import Prediction

@login_required
def dashboard(request):
    total_customers = Customer.objects.count()
    
    latest_predictions = Prediction.objects.filter(
        customer=OuterRef('pk')
    ).order_by('-created_at')
    
    customers_with_risk = Customer.objects.annotate(
        latest_risk=Subquery(latest_predictions.values('risk_level')[:1])
    )
    
    high_risk_count = customers_with_risk.filter(latest_risk='HIGH').count()
    medium_risk_count = customers_with_risk.filter(latest_risk='MEDIUM').count()
    low_risk_count = customers_with_risk.filter(latest_risk='LOW').count()
    
    recent_predictions = Prediction.objects.select_related('customer').order_by('-created_at')[:10]

    context = {
        'total_customers': total_customers,
        'high_risk_count': high_risk_count,
        'medium_risk_count': medium_risk_count,
        'low_risk_count': low_risk_count,
        'recent_predictions': recent_predictions,
    }
    return render(request, 'dashboard/index.html', context)

from django.db.models import Prefetch

@login_required
def customer_list(request):
    latest_prediction = Prediction.objects.order_by('-created_at')
    customers = Customer.objects.prefetch_related(
        Prefetch('predictions', queryset=latest_prediction, to_attr='latest_predictions')
    ).order_by('-created_at')
    return render(request, 'customers/customer_list.html', {'customers': customers})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Customer created successfully.')
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'action': 'Create'})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'action': 'Update'})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully.')
        return redirect('customers:customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})


