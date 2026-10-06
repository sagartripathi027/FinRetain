from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from customers import views as customer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', customer_views.signup, name='signup'),
    
    # Dashboard
    path('', customer_views.dashboard, name='dashboard'),
    
    # App URLs
    path('customers/', include('customers.urls')),
    path('predictions/', include('predictions.urls')),
]

