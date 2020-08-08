from rest_framework import viewsets

from shopping_list import serializers, models, permissions


class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = models.ShoppingList.objects.all()
    serializer_class = serializers.ShoppingListSerializer
    permission_classes = [permissions.IsOwnerOrSuperuser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset() if user.is_superuser else models.ShoppingList.objects.filter(owner=user)
