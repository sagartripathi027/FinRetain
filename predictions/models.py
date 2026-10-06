from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from customers.models import Customer

class Prediction(models.Model):
    RISK_LEVEL_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='predictions')
    churn_probability = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Probability of churn (0.0 to 1.0)"
    )
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    prediction = models.BooleanField(help_text="True if likely to churn")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Prediction for {self.customer.name} - {self.risk_level} Risk"

class RetentionRecommendation(models.Model):
    prediction = models.OneToOneField(Prediction, on_delete=models.CASCADE, related_name='recommendation')
    recommendation = models.CharField(max_length=255)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.prediction.customer.name}"

