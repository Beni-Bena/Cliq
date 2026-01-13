from django.shortcuts import render, get_object_or_404
from .models import Vendor, Product
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Vendor
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Vendor, Product


# Create your views here.
def index(request):
    # Détecter quel formulaire afficher (signup ou login) depuis le paramètre GET
    active_form = request.GET.get('form', 'signup')
    context = {
        'active_form': active_form
    }
    return render(request, 'index.html', context)

def shop(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug, is_active=True)

    # Récupérer l'abonnement s'il existe
    subscription = getattr(vendor, "subscription", None)

    # Vérifier l'abonnement
    if not subscription or not subscription.is_valid():
        return render(request, "index.html", {
            "vendor": vendor,
            "message": "Votre abonnement n'est pas actif ou a expiré."
        })

    # Limiter les produits selon l'abonnement
    max_products = getattr(subscription, "max_products", 0)
    products = vendor.products.filter(is_available=True)[:max_products]

    return render(request, "shop.html", {
    "vendor": vendor,        # Le vendeur actif
    "products": products,    # La liste des produits disponibles
    "subscription": subscription  # Optionnel si tu veux afficher les infos d'abonnement
})



def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        shop_name = request.POST.get('shop_name')
        whatsapp = request.POST.get('whatsapp')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        terms = request.POST.get('terms')

        # Vérifications de base
        if not terms:
            messages.error(request, "Vous devez accepter les conditions d'utilisation.")
            return redirect(reverse('index') + '?form=signup')

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect(reverse('index') + '?form=signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Un compte avec cet email existe déjà.")
            return redirect(reverse('index') + '?form=signup')

        # Création de l'utilisateur
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password1, 
            first_name=full_name
        )

        # Création du Vendor
        Vendor.objects.create(
            user=user,
            shop_name=shop_name,
            whatsapp_number=whatsapp
        )

        # Lien vers le login (page de connexion)
        login_url = request.build_absolute_uri(reverse('index') + '?form=login')

        # Contexte à envoyer à la page bienvenue.html
        context = {
            'full_name': full_name,
            'shop_name': shop_name,
            'whatsapp': whatsapp,
            'email': email,
            'login_url': login_url,
        }

        # Redirection vers bienvenue.html
        return render(request, 'bienvenue.html', context)

    # Si GET, retourne à l'accueil
    return redirect('index')

def login(request):
    if request.method == 'POST':
        username_or_whatsapp = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        # Auth par email / username
        user = authenticate(
            request,
            username=username_or_whatsapp,
            password=password
        )

        # Si échec → tentative par WhatsApp
        if user is None:
            try:
                vendor = Vendor.objects.get(
                    whatsapp_number=username_or_whatsapp
                )
                user = authenticate(
                    request,
                    username=vendor.user.username,
                    password=password
                )
            except Vendor.DoesNotExist:
                user = None

        if user is not None:
            auth_login(request, user)

            # Gestion remember me
            if remember:
                request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                request.session.set_expiry(0)

            return redirect('vendor_dashboard')

        messages.error(request, "Identifiants invalides.")
        return redirect(reverse('index') + '?form=login')

    return redirect('index')

@login_required
def vendor_dashboard(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(
            request,
            "Ce compte n'est pas associé à un vendeur."
        )
        return redirect('logout')

    products = Product.objects.filter(
        vendor=vendor,
        is_available=True
    )

    return render(request, 'produit.html', {
        'vendor': vendor,
        'products': products,
    })


def logout_view(request):
    logout(request)
    return redirect('index')





@login_required
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price")
        image = request.FILES.get("image")

        # Sécurité minimale
        if not all([name, price, image]):
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return redirect("add_product")

        product = Product.objects.create(
            vendor=request.user.vendor,
            name=name,
            price=price,
            image=image
        )

        # Si le champ existe dans ton modèle
        if hasattr(product, "description"):
            product.description = description
            product.save()

        messages.success(request, "Produit ajouté avec succès.")
        return redirect("vendor_dashboard")

    return render(request, "products/add_product.html")

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        # -------- TEXT FIELDS --------
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()

        # -------- IMAGE --------
        image = request.FILES.get("image")

        modified = False  # pour savoir s'il y a eu modification

        # Nom
        if name and name != product.name:
            product.name = name
            modified = True

        # Description (si ton modèle l'a)
        if hasattr(product, "description"):
            if description != product.description:
                product.description = description
                modified = True

        # Prix
        if price:
            price = float(price)
            if price != product.price:
                product.price = price
                modified = True

        # Image (uniquement si l'utilisateur a choisi une nouvelle)
        if image:
            product.image = image
            modified = True

        # -------- SAUVEGARDE --------
        if modified:
            product.save()
            messages.success(request, "Produit modifié avec succès.")
        else:
            messages.info(request, "Aucune modification détectée.")

        return redirect("vendor_dashboard")

    return render(request, "produit.html", {
        "product": product
    })


def delete_product(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        vendor=request.user.vendor
    )

    if request.method == "POST":
        product.delete()
        messages.success(request, "Produit supprimé avec succès.")
        return redirect("vendor_dashboard")

    messages.error(request, "Action non autorisée.")
    return redirect("vendor_dashboard")





