from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def common_context():
    return {
        "nav_categories": Category.objects.all(),
    }


def home(request):
    context = {
        "title": "TechStore",
        "subtitle": "Reliable laptops, phones, and accessories for everyday use.",
        "categories": Category.objects.prefetch_related("products"),
        "featured_products": Product.objects.select_related("category").filter(is_available=True)[:6],
        "pages": [
            {"title": "About us", "url_name": "shop:about"},
            {"title": "Catalog", "url_name": "shop:catalog"},
            {"title": "Contacts", "url_name": "shop:contacts"},
        ],
    }
    context.update(common_context())
    return render(request, "shop/home.html", context)


def about(request):
    context = {
        "title": "About TechStore",
        "text": "We help customers choose reliable devices for study, work, and home.",
    }
    context.update(common_context())
    return render(request, "shop/simple_page.html", context)


def catalog(request):
    selected_category = request.GET.get("category")
    products = Product.objects.select_related("category").filter(is_available=True)

    if selected_category:
        products = products.filter(category__slug=selected_category)

    context = {
        "title": "Catalog",
        "products": products,
        "categories": Category.objects.all(),
        "selected_category": selected_category,
    }
    context.update(common_context())
    return render(request, "shop/catalog.html", context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_available=True)
    context = {
        "title": category.name,
        "category": category,
        "products": products,
    }
    context.update(common_context())
    return render(request, "shop/category_detail.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug, is_available=True)
    context = {
        "title": product.name,
        "product": product,
    }
    context.update(common_context())
    return render(request, "shop/product_detail.html", context)


def contacts(request):
    context = {
        "title": "Contacts",
        "text": "Email: info@techstore.local | Phone: +380 00 000 00 00",
    }
    context.update(common_context())
    return render(request, "shop/simple_page.html", context)

# Create your views here.
