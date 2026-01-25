import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r"users", views.UserViewSet, basename="user")
router.register(r"collects", views.CollectViewSet, basename="collect")
router.register(r"payments", views.PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]
