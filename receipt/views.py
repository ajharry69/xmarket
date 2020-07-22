from rest_framework import viewsets, parsers
from xauth.permissions import IsOwnerOrSuperuser

from receipt import serializers, models


class ReceiptsViewSet(viewsets.ModelViewSet):
    queryset = models.Receipt.objects.all()
    serializer_class = serializers.ReceiptSerializer
    permission_classes = [IsOwnerOrSuperuser]
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser, ]

    def get_queryset(self):
        user = self.request.user
        return models.Receipt.objects.all() if user.is_superuser else models.Receipt.objects.filter(owner=user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
