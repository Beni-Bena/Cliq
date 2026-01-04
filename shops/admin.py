from django.contrib import admin
from .models import Vendor, Product, SubscriptionPlan, VendorSubscription

admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(SubscriptionPlan)
admin.site.register(VendorSubscription)
