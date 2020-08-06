import json

from rest_framework import viewsets, parsers, status
from rest_framework.response import Response
from xauth import permissions

from article import serializers, models


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser,)
    permission_classes = (permissions.IsOwnerOrSuperuserOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self._create_write_serializer(request)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED,
                            headers=self.get_success_headers(serializer.data))
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        serializer = self._create_write_serializer(request, self.get_object())
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK,
                            headers=self.get_success_headers(serializer.data))
        return super().update(request, *args, **kwargs)

    def _create_write_serializer(self, request, instance=None):
        media, article = None, request.data.get('article') or request.data
        article = json.loads(article) if isinstance(article, (str, bytes)) else article
        try:
            media = request.data.getlist('media')
        except AttributeError:
            pass
        return serializers.ArticleRequestSerializer(
            instance=instance,
            data={'article': article, 'media': media},
            context=self.get_serializer_context(),
        )
