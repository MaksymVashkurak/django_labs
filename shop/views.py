from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NewsletterSubscriptionForm, RatingForm
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
        "newsletter_form": NewsletterSubscriptionForm(),
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

    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.product = product
            rating.save()
            messages.success(request, "Thank you for rating this product.")
            return redirect(product.get_absolute_url())
    else:
        rating_form = RatingForm()

    context = {
        "title": product.name,
        "product": product,
        "rating_form": rating_form,
        "ratings": product.ratings.all()[:5],
    }
    context.update(common_context())
    return render(request, "shop/product_detail.html", context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_available=True)
    cart = request.session.get("cart", {})
    product_key = str(product.id)
    cart[product_key] = cart.get(product_key, 0) + 1
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to cart.")
    return redirect("shop:cart_detail")


def cart_detail(request):
    cart = request.session.get("cart", {})
    product_ids = [int(product_id) for product_id in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    items = []
    total = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)
        item_total = product.price * quantity
        total += item_total
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "total": item_total,
            }
        )

    context = {
        "title": "Cart",
        "items": items,
        "total": total,
    }
    context.update(common_context())
    return render(request, "shop/cart.html", context)


def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You subscribed to TechStore news.")
        else:
            messages.error(request, "Please check newsletter form data.")
    return redirect("shop:home")


def contacts(request):
    context = {
        "title": "Contacts",
        "text": "Email: info@techstore.local | Phone: +380 00 000 00 00",
    }
    context.update(common_context())
    return render(request, "shop/simple_page.html", context)

# Create your views here.
