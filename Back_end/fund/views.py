from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from fund.models import Fund, FundTransaction
from fund.serializers import FundSerializer, FundTransactionSerializer
from accounts.permissions import IsHeadMaster


class FundViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated, IsHeadMaster]


class FundTransactionViewSet(viewsets.ModelViewSet):
    queryset = FundTransaction.objects.all()
    serializer_class = FundTransactionSerializer
    permission_classes = [IsAuthenticated, IsHeadMaster]

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
