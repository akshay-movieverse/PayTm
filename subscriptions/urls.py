

from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('save-subscription/', views.save_subscription_view, name='save_subscription'),
    path('success/', views.subscription_success_view, name='subscription_success'),
    path('cancel/', views.subscription_cancel_view, name='subscription_cancel'),
    path('webhook/', views.paypal_webhook_view, name='paypal_webhook'), # Webhook endpoint

        path('login/', views.login, name='login'),

        path('', views.home, name='dashboard'),
]