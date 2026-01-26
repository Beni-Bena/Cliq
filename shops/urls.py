from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path("@<slug:slug>/", views.shop, name="shop"),
    #path("@<slug:slug>/<slug:product_slug>/", views.produit, name="produit"),
    path("login/", views.login, name="login"),
    path("register_vendor/", views.register, name="register"),
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path("product/add/", views.add_product, name="add_product"),
    path("product/<int:product_id>/edit/", views.edit_product, name="edit_product"), 
    path("product/<int:product_id>/delete/",views.delete_product,name="delete_product"),
    path("update_profile/", views.update_profile, name="update_profile"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)