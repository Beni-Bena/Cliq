from django.contrib import admin
from .models import Vendor, Product,VendorSubscription

admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(VendorSubscription)
