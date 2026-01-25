import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Collect, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email"]

        # Метод создаёт пользователя с хешированным паролем, если данные валидны
        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user


class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    collect_title = serializers.CharField(source="collect.title", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "collect",
            "collect_title",
            "user",
            "user_name",
            "user_username",
            "amount",
            "comment",
            "created_at",
            "is_anonymous",
        ]
        read_only_fields = ["id", "created_at"]

    def to_representation(
        self, instance
    ):  # Переопределяем формат вывода анонимного платежа - указываем значения полей модели.
        data = super().to_representation(instance)
        if instance.is_anonymous:
            data["user_name"] = "Аноним"
            data["user_username"] = "anonymous"
            data["user"] = None
        return data


class CollectSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    payments_count = serializers.IntegerField(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Collect
        fields = [
            "id",
            "author",
            "author_name",
            "author_username",
            "title",
            "occasion",
            "description",
            "target_amount",
            "collected_amount",
            "cover_image",
            "end_date",
            "created_at",
            "updated_at",
            "is_active",
            "payments_count",
            "payments",
            "cover_image_url",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "collected_amount"]

    def get_cover_image_url(
        self, obj
    ):  # Получение URL обложки платежа для вывода в API
        if obj.cover_image:
            return obj.cover_image.url
        return None

    def validate_end_date(self, value):  # Валидация даты сбора
        from django.utils import timezone

        if value <= timezone.now():
            raise serializers.ValidationError(
                "Дата завершения должна быть больше текущей даты"
            )
        return value


class CollectListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    payments_count = serializers.IntegerField(read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Collect
        fields = [
            "id",
            "author_name",
            "title",
            "occasion",
            "collected_amount",
            "target_amount",
            "cover_image",
            "end_date",
            "is_active",
            "payments_count",
            "cover_image_url",
            "progress_percentage",
        ]

    def get_cover_image_url(
        self, obj
    ):  # Получение URL обложки платежа для вывода в API
        if obj.cover_image:
            return obj.cover_image.url
        return None

    def get_progress_percentage(
        self, obj
    ):  # Расчёт %% текущей суммы от цели сбора для вывода в API
        if obj.target_amount and obj.target_amount > 0:
            if obj.collected_amount:
                return min(
                    round((obj.collected_amount / obj.target_amount) * 100, 1), 100
                )
            else:
                return 0
        return f"Целевая сумма сбора не назначена"


# Сериалайзер для создания платежа на странице сбора
class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["amount", "comment", "is_anonymous"]
