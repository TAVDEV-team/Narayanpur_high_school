from rest_framework.routers import DefaultRouter
from django.urls import path, include

from fund.views import FundViewSet, FundTransactionViewSet

router = DefaultRouter()
router.register(r'fund', FundViewSet, basename='fund')
router.register(r'transactions', FundTransactionViewSet, basename='transactions')


urlpatterns = [
    path('', include(router.urls)),
]
