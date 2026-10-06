from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customers.models import Customer
from .services import run_churn_prediction

@login_required
def run_prediction_view(request, pk):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, pk=pk)
        try:
            prediction = run_churn_prediction(customer)
            messages.success(request, f"Prediction updated successfully. Risk level: {prediction.risk_level}")
        except Exception as e:
            messages.error(request, f"Failed to run prediction: {str(e)}")
        
        return redirect('customers:customer_detail', pk=pk)
    else:
        return redirect('customers:customer_detail', pk=pk)

