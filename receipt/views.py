from rest_framework import viewsets, parsers, pagination
from rest_framework.response import Response
from xauth.permissions import IsOwnerOrSuperuser

from receipt import serializers, models


class ReceiptsViewSet(viewsets.ModelViewSet):
    queryset = models.Receipt.objects.all()
    serializer_class = serializers.ReceiptSerializer
    permission_classes = [IsOwnerOrSuperuser]
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser, ]
    pagination_class = pagination.LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self._transform_list_data(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return Response(self._transform_list_data(serializer.data))

    @staticmethod
    def _transform_list_data(data):
        return [receipt['url'] for receipt in data]

    def get_queryset(self):
        user = self.request.user
        return models.Receipt.objects.all() if user.is_superuser else models.Receipt.objects.filter(owner=user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
