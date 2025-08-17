from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny

# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from accounts.permissions import IsHeadMaster
from fund.models import Fund, FundTransaction
from fund.serializers import FundSerializer, FundTransactionSerializer


class FundViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, IsHeadMaster]
    # permission_classes = [IsAuthenticated]


@method_decorator(cache_page(60 * 5), name="list")  # cache list view 5 mins
@method_decorator(
    cache_page(60 * 5), name="retrieve"
)  # cache detail view 5 mins
class FundTransactionViewSet(viewsets.ModelViewSet):
    queryset = FundTransaction.objects.all()
    serializer_class = FundTransactionSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, IsHeadMaster]

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Update not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Deletion not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
