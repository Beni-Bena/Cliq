from django.shortcuts import render, get_object_or_404
from .models import Vendor, Product
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Vendor
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Vendor, Product,ProductImage
from django.utils.text import slugify



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

def abonnement(request):
    return render(request, 'abonnement.html')

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
        currency = request.POST.get("currency")

        images = request.FILES.getlist("images")  

        if not all([name, price, currency]):
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return redirect("vendor_dashboard")

        if len(images) == 0:
            messages.error(request, "Veuillez ajouter au moins une image.")
            return redirect("vendor_dashboard")

        if len(images) > 5:
            messages.error(request, "Maximum 5 images autorisées.")
            return redirect("vendor_dashboard")

        product = Product.objects.create(
            vendor=request.user.vendor,
            name=name,
            description=description,
            price=price,
            currency=currency
        )
        for img in images:
            ProductImage.objects.create(
                product=product,
                image=img
            )

        messages.success(request, "Produit ajouté avec succès.")
        return redirect("vendor_dashboard")



@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.vendor.user != request.user:
        messages.error(request, "Accès non autorisé.")
        return redirect("vendor_dashboard")

    if request.method == "POST":

        modified = False

        # -------- TEXT FIELDS --------
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price")
        currency = request.POST.get("currency")

        if name and name != product.name:
            product.name = name
            modified = True

        if description != (product.description or ""):
            product.description = description
            modified = True

        if price:
            try:
                price = float(price)
                if price != float(product.price):
                    product.price = price
                    modified = True
            except ValueError:
                messages.error(request, "Prix invalide.")
                return redirect("vendor_dashboard")

        if currency and currency != product.currency:
            product.currency = currency
            modified = True

        # -------- DELETE IMAGES --------
        delete_images = request.POST.getlist("delete_images")
        if delete_images:
            ProductImage.objects.filter(
                id__in=delete_images,
                product=product
            ).delete()
            modified = True

        # -------- ADD NEW IMAGES --------
        new_images = request.FILES.getlist("images")

        if new_images:
            existing_count = product.images.count()
            available_slots = 5 - existing_count

            if available_slots <= 0:
                messages.error(request, "Nombre maximum d’images atteint (5).")
                return redirect("vendor_dashboard")

            for img in new_images[:available_slots]:
                ProductImage.objects.create(
                    product=product,
                    image=img
                )
                modified = True

            if product.image:
                product.image = None

        # -------- SAVE --------
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



@login_required
def update_profile(request):
    user = request.user

    try:
        vendor = user.vendor
    except Vendor.DoesNotExist:
        messages.error(request, "Profil vendeur introuvable.")
        return redirect("home")

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        if not user.check_password(current_password):
            messages.error(request, "Mot de passe incorrect.")
            return redirect("vendor_dashboard")
        shop_name = request.POST.get("shop_name", "").strip()
        slug_input = request.POST.get("slug", "").strip()
        whatsapp_number = request.POST.get("whatsapp_number", "").strip()
        email = request.POST.get("email", "").strip()

        if not shop_name or not whatsapp_number or not slug_input:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return redirect("vendor_dashboard")
        vendor.shop_name = shop_name
        vendor.whatsapp_number = whatsapp_number
        if slug_input != vendor.slug:
            base_slug = slugify(slug_input)
            slug = base_slug
            count = 1
            while Vendor.objects.filter(slug=slug).exclude(id=vendor.id).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            vendor.slug = slug

        vendor.save()

        if email and email != user.email:
            user.email = email
            user.save()

        messages.success(request, "Profil mis à jour avec succès.")
        return redirect("vendor_dashboard")

    return render(request, "produit.html", {
        "vendor": vendor
    })





