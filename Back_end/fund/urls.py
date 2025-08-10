from django.urls import include, path
from rest_framework.routers import DefaultRouter

from fund.views import FundTransactionViewSet, FundViewSet

router = DefaultRouter()
router.register(r"balance", FundViewSet, basename="fund")
router.register(
    r"transactions", FundTransactionViewSet, basename="transactions"
)


urlpatterns = [
    path("", include(router.urls)),
]
