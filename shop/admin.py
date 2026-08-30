from django.contrib import admin

from .models import Category, NewsletterSubscription, Order, OrderItem, PasswordResetCode, Product, Rating


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "created_at", "updated_at")
    list_filter = ("category", "is_available")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "email", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "email", "phone")
    inlines = [OrderItemInline]


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "created_at", "updated_at")
    search_fields = ("email", "name")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "score", "created_at", "updated_at")
    list_filter = ("score", "created_at")
    search_fields = ("product__name", "name", "comment")


@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "is_used", "created_at", "updated_at")
    list_filter = ("is_used", "created_at")
    search_fields = ("user__username", "user__email", "code")

# Register your models here.
