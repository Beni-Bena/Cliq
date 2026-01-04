from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # ex: beni
    whatsapp_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def shop_url(self):
        return f"/@{self.slug}"

    def __str__(self):
        return self.shop_name



class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def whatsapp_link(self):
        message = f"Bonjour, je suis intéressé par le produit {self.name}"
        return f"https://wa.me/{self.vendor.whatsapp_number}?text={message}"

    def __str__(self):
        return self.name


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)  # Free, Pro, Premium
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    max_products = models.IntegerField()

    def __str__(self):
        return self.name

class VendorSubscription(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.end_date >= timezone.now()

    def __str__(self):
        return f"{self.vendor.shop_name} - {self.plan.name}"
