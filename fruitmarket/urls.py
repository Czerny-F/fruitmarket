from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .core import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('products/', include('fruitmarket.apps.products.urls')),
    path('sales/', include('fruitmarket.apps.sales.urls')),
    path('admin/', admin.site.urls),
]
