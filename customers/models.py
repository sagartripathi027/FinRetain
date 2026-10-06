from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Customer(models.Model):
    customer_id = models.CharField(max_length=50, unique=True, help_text="Unique identifier for the customer")
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    # Aggregated ML features
    tenure = models.PositiveIntegerField(help_text="Tenure in months", default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    transaction_frequency = models.PositiveIntegerField(help_text="Transactions per month", default=0)
    complaints = models.PositiveIntegerField(help_text="Number of complaints", default=0)
    service_usage = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Service usage score (0.0 to 1.0)",
        default=0.0
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.customer_id})"

