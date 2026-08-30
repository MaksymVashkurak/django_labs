import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CheckoutForm,
    NewsletterSubscriptionForm,
    PasswordResetConfirmForm,
    PasswordResetRequestForm,
    RatingForm,
    RegisterForm,
)
from .models import Category, OrderItem, PasswordResetCode, Product


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


@login_required
def checkout(request):
    cart = request.session.get("cart", {})
    product_ids = [int(product_id) for product_id in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid() and products:
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for product in products:
                quantity = cart.get(str(product.id), 0)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                )
            request.session["cart"] = {}
            messages.success(request, "Order created successfully.")
            return redirect("shop:profile")
    else:
        form = CheckoutForm(
            initial={
                "customer_name": request.user.get_username(),
                "email": request.user.email,
            }
        )

    context = {
        "title": "Checkout",
        "form": form,
        "has_items": bool(products),
    }
    context.update(common_context())
    return render(request, "shop/checkout.html", context)


def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You subscribed to TechStore news.")
        else:
            messages.error(request, "Please check newsletter form data.")
    return redirect("shop:home")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration completed.")
            return redirect("shop:profile")
    else:
        form = RegisterForm()

    context = {"title": "Register", "form": form}
    context.update(common_context())
    return render(request, "shop/auth_form.html", context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("shop:profile")
    else:
        form = AuthenticationForm()

    context = {"title": "Login", "form": form}
    context.update(common_context())
    return render(request, "shop/auth_form.html", context)


def logout_view(request):
    logout(request)
    return redirect("shop:home")


@login_required
def profile(request):
    if request.user.is_staff:
        orders = OrderItem.objects.select_related("order", "product").all()
        title = "All orders"
    else:
        orders = OrderItem.objects.select_related("order", "product").filter(order__user=request.user)
        title = "My orders"

    context = {
        "title": "Profile",
        "orders_title": title,
        "order_items": orders,
    }
    context.update(common_context())
    return render(request, "shop/profile.html", context)


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                code = f"{random.randint(100000, 999999)}"
                PasswordResetCode.objects.create(user=user, code=code)
                send_mail(
                    "TechStore password reset",
                    f"Your temporary password reset code is: {code}",
                    "noreply@techstore.local",
                    [email],
                )
            messages.success(request, "If this email exists, a reset code was sent.")
            return redirect("shop:password_reset_confirm")
    else:
        form = PasswordResetRequestForm()

    context = {"title": "Password reset", "form": form}
    context.update(common_context())
    return render(request, "shop/auth_form.html", context)


def password_reset_confirm(request):
    if request.method == "POST":
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            code = form.cleaned_data["code"]
            reset_code = PasswordResetCode.objects.filter(
                user__email=email,
                code=code,
                is_used=False,
            ).select_related("user").first()

            if reset_code:
                reset_code.user.set_password(form.cleaned_data["new_password"])
                reset_code.user.save()
                reset_code.is_used = True
                reset_code.save()
                messages.success(request, "Password changed successfully.")
                return redirect("shop:login")
            messages.error(request, "Invalid reset code.")
    else:
        form = PasswordResetConfirmForm()

    context = {"title": "Confirm password reset", "form": form}
    context.update(common_context())
    return render(request, "shop/auth_form.html", context)


def contacts(request):
    context = {
        "title": "Contacts",
        "text": "Email: info@techstore.local | Phone: +380 00 000 00 00",
    }
    context.update(common_context())
    return render(request, "shop/simple_page.html", context)

# Create your views here.
