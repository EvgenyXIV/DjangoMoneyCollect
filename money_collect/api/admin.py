import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
from django.contrib import admin
from .models import Collect, Payment

# Register your models here.


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "occasion",
        "collected_amount",
        "target_amount",
        "end_date",
        "is_active",
        "payments_count",
        "created_at",
    ]
    list_filter = ["occasion", "created_at", "end_date", "author"]
    search_fields = ["title", "description", "author__username"]
    readonly_fields = ["collected_amount", "created_at", "updated_at", "payments_count"]
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("author", "title", "occasion", "description")},
        ),
        (
            "Финансы",
            {"fields": ("target_amount", "collected_amount", "payments_count")},
        ),
        (
            "Медиа и даты",
            {"fields": ("cover_image", "end_date", "created_at", "updated_at")},
        ),
    )

    def is_active(self, obj):
        return obj.is_active

    is_active.boolean = True
    is_active.short_description = "Активен"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "collect",
        "amount",
        "created_at",
        "is_anonymous",
        "get_user_name",
    ]
    list_filter = ["created_at", "is_anonymous", "collect"]
    search_fields = ["user__username", "collect__title", "comment"]
    readonly_fields = ["created_at"]

    def get_user_name(self, obj):
        if obj.is_anonymous:
            return "Аноним"
        return obj.user.get_full_name() or obj.user.username

    get_user_name.short_description = "Имя пользователя"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "collect")
