from django.urls import include, path
from fund.views import FundTransactionViewSet, FundViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"balance", FundViewSet, basename="fund")
router.register(
    r"transactions", FundTransactionViewSet, basename="transactions"
)


urlpatterns = [
    path("", include(router.urls)),
]
