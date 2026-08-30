from django.shortcuts import render


def home(request):
    context = {
        "title": "TechStore",
        "subtitle": "Online store for laptops, phones, and accessories",
        "pages": [
            {"title": "About us", "url_name": "shop:about"},
            {"title": "Contacts", "url_name": "shop:contacts"},
        ],
    }
    return render(request, "shop/home.html", context)


def about(request):
    context = {
        "title": "About TechStore",
        "text": "We help customers choose reliable devices for study, work, and home.",
    }
    return render(request, "shop/simple_page.html", context)


def contacts(request):
    context = {
        "title": "Contacts",
        "text": "Email: info@techstore.local | Phone: +380 00 000 00 00",
    }
    return render(request, "shop/simple_page.html", context)

# Create your views here.
