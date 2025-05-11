from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings # To get the User model
from django.contrib.auth.models import User

class Subscription(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending'), # Initial state before confirmation
        ('EXPIRED', 'Expired'),
        ('SUSPENDED', 'Suspended'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    paypal_subscription_id = models.CharField(max_length=100, unique=True, help_text="PayPal's Subscription ID")
    paypal_plan_id = models.CharField(max_length=100, help_text="PayPal Plan ID used for this subscription")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    start_date = models.DateTimeField(null=True, blank=True)
    next_billing_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.paypal_subscription_id} ({self.status})"