from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Vendor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="vendor"
    )

    shop_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    whatsapp_number = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.shop_name)
            slug = base_slug
            count = 1
            while Vendor.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def shop_url(self):
        return f"/@{self.slug}/"

    def __str__(self):
        return self.shop_name

class Product(models.Model):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while Product.objects.filter(
                vendor=self.vendor,
                slug=slug
            ).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


from django.utils import timezone
from datetime import timedelta

class VendorSubscription(models.Model):

    FREE = "free"
    PRO = "pro"

    PLAN_CHOICES = [
        (FREE, "Gratuit"),
        (PRO, "Pro"),
    ]

    vendor = models.OneToOneField(
        Vendor,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    plan = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES,
        default=FREE
    )

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    max_products = models.IntegerField(default=5)

    def save(self, *args, **kwargs):
        if self.plan == self.PRO and not self.end_date:
            self.end_date = self.start_date + timedelta(days=30)

        if self.plan == self.FREE:
            self.end_date = None
            self.max_products = 5

        super().save(*args, **kwargs)

    def is_valid(self):
        if self.plan == self.FREE:
            return True
        return self.end_date and self.end_date >= timezone.now()

    def __str__(self):
        return f"{self.vendor.shop_name} - {self.plan}"
