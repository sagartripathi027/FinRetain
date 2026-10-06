from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('run/<int:pk>/', views.run_prediction_view, name='run_prediction'),
]
