from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("catalog/", views.catalog, name="catalog"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("newsletter/", views.subscribe_newsletter, name="subscribe_newsletter"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("contacts/", views.contacts, name="contacts"),
]
