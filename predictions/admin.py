from django.contrib import admin
from .models import Prediction, RetentionRecommendation

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'churn_probability', 'risk_level', 'prediction', 'created_at')
    list_filter = ('risk_level', 'prediction', 'created_at')
    search_fields = ('customer__name', 'customer__customer_id')

@admin.register(RetentionRecommendation)
class RetentionRecommendationAdmin(admin.ModelAdmin):
    list_display = ('prediction', 'recommendation', 'created_at')
    search_fields = ('prediction__customer__name', 'recommendation')

