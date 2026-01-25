import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)  # Для фильтрации по полям модели
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)  # Для фильтрации и сортировки по полям модели
from django.contrib.auth.models import User
from .models import Collect, Payment  # Импортируем модели Collect и Payment
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    CollectSerializer,
    CollectListSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
)
from django.utils import timezone  # Для работы с временем

# Подключаем функции для отправки уведомлений (если не используются сигналы)
# from .utils.email_utilities import send_collect_created, send_payment_created, send_collect_updated, send_payment_updated

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by(
        "-date_joined"
    )  # Получение всех пользователей, сначала новые
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Только для чтения (если не авторизован)

    def get_permissions(self):  # Встроенный метод для установки прав доступа
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [
                IsAdminUser()
            ]  # Только админ может создавать, изменять, удалять пользователя
        return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):  # Переопределяем функцию для выбора сериализатора
        if self.action == "me":  # Если действие - создание пользователя
            return UserCreateSerializer  # сериализатор при создании пользователя
        else:
            return UserSerializer  # сериализатор просмотра списка пользователей

    # Extra Action 'Me' на уровне API списка сборов (detail=False), методы 'post', 'get', 'put'
    # Вывод и изменение текущего и ввод нового пользователя
    @action(detail=False, methods=["POST", "PUT", "GET", "DELETE"])
    def me(self, request):
        if request.method in ["POST", "PUT", "DELETE"]:
            self.permission_classes = [
                IsAdminUser
            ]  # Создание и изменение пользователя только админом
        self.check_permissions(request)
        serializer = UserCreateSerializer(request.user)
        return Response(serializer.data)


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()  # Получение всех сборов в список queryset
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Только для чтения (если не авторизован)
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]  # Для фильтрации, поиска и сортировки по на API-странице сборов
    filterset_fields = ["occasion", "author"]  # Поля фильтрации
    search_fields = [
        "title",
        "description",
    ]  # Поля поиска. Поиск будет по полям title и description
    ordering_fields = ["created_at", "collected_amount", "end_date"]  # Поля сортировки
    ordering = [
        "-created_at"
    ]  # Сортировка по умолчанию по полю created_at в обратном порядке

    # Выбор сериалайзера данных для списка сборов в зависимости от действия
    def get_serializer_class(self):
        if self.action == "donate":
            return PaymentCreateSerializer
        elif self.action == "list":
            return CollectListSerializer
        return CollectSerializer

    # Функция для создания сбора (и отправка уведомления, если не используются сигналы - закоммичено)
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )  # Сохранение сбора в БД, автор - текущий пользователь
        # if not send_collect_created.delay(instance.id):                           # Отправка уведомления о создании сбора
        #     raise Exception("Не удалось отправить уведомление о создании сбора")  # Обработка исключения

    # Extra Action 'Donate' на уровне API конкретного сбора (detail=True)
    # Ввод нового платежа, доступен POST-запрос для авторизованных пользователей
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def donate(
        self, request, pk=None
    ):  # Отправка POST-запроса на платёж на API-странице сбора
        collect = (
            self.get_object()
        )  # Встроенный родительский метод получения объекта сбора по текущему id
        serializer = PaymentCreateSerializer(
            data=request.data
        )  # Сериализатор для создания платежа

        if serializer.is_valid():  # Проверка валидности данных сериализатора
            payment = serializer.save(
                collect=collect, user=request.user
            )  # Сохранение платежа в экземпляр объекта payment
            payment_serializer = PaymentSerializer(
                payment
            )  # Сериализатор для вывода результатов платежа в ответе на запрос
            return Response(
                payment_serializer.data, status=status.HTTP_201_CREATED
            )  # Возвращается ответ с данными платежа и статусом 201 (создан)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Extra Action 'Payments' на уровне API конкретного сбора (detail=True)
    # Вывод всех платежей на уровне API только для текущего сбора, доступно только при GET-запросе
    @action(detail=True, methods=["get"])
    def payments(self, request, pk=None):
        collect = self.get_object()  # Получение конкретного сбора по id
        payments = collect.payments.all()
        page = self.paginate_queryset(payments)

        if page is not None:
            serializer = PaymentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    # Extra Action 'Active' на уровне API списка сборов, доступно при GET-запросе
    # Вывод всех (detail=False) активных сборов на странице
    @action(detail=False, methods=["get"])
    def active(self, request):
        active_collects = self.queryset.filter(
            end_date__gte=timezone.now()
        )  # Фильтр end_date=>текущее время
        page = self.paginate_queryset(
            active_collects
        )  # Пагинация возвращает None, если пагинация не активна,
        # или первую страницу в случае, если пагинация нужна
        if page is not None:
            serializer = CollectListSerializer(
                page, many=True
            )  # Если пагинация нужна, то сериализуем данные
            return self.get_paginated_response(
                serializer.data
            )  # и пагинация продолжается

        serializer = CollectListSerializer(
            active_collects, many=True
        )  # Eсли пагинация не нужна, то просто сериализуем
        return Response(serializer.data)  # и возвращаем обычный ответ


# Для вывода платежей пользователя
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()  # Получение всех платежей
    serializer_class = PaymentSerializer  # Сериализатор
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Только для чтения (если не авторизован)
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]  # Для фильтрации и сортировки по полям модели
    filterset_fields = ["collect", "user", "is_anonymous"]  # Поля фильтрации
    ordering_fields = ["created_at", "amount"]  # Поля сортировки
    ordering = ["-created_at"]  # Сортировка по полю created_at в обратном порядке

    def get_queryset(
        self,
    ):  # Выполняется запрос платежей с фильтрацией по текущему пользователю
        if self.request.user.is_authenticated:
            return Payment.objects.filter(
                user=self.request.user
            )  # Вывод всех платежей авторизованного пользователя
        return Payment.objects.filter(
            is_anonymous=True
        )  # Неавторизованный пользователь увидит только публичные (анонимные) платежи

    # Функция для создания платежа, сбор и донатер на выбор (и отправка уведомления, если не используются сигналы)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Сохранение платежа в БД
        # if not send_payment_created.delay(instance.id):     # Отправка уведомления о выполнении платежа
        #     raise Exception("Не удалось отправить уведомление о выполнении платежа")    # Обработка исключения
