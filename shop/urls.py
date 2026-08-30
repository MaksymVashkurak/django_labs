from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("catalog/", views.catalog, name="catalog"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("contacts/", views.contacts, name="contacts"),
]
