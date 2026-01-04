from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .models import Vendor
# Create your views here.
def index(request):
    return render(request, 'index.html')

def shop(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug, is_active=True)

    # abonnement
    try:
        subscription = vendor.vendorsubscription
    except:
        subscription = None

    # si pas d'abonnement ou expiré
    if not subscription or not subscription.is_valid():
        return render(request, "shop_expired.html", {
            "vendor": vendor
        })

    # produits limités selon l'abonnement
    max_products = subscription.plan.max_products
    products = vendor.products.filter(is_available=True)[:max_products]

    return render(request, "shop.html", {
        "vendor": vendor,
        "products": products,
        "subscription": subscription
    })
