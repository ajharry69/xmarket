import json

from rest_framework import viewsets, parsers, status
from rest_framework.decorators import action
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

    @action(detail=True, description="[un-]flag an article as appropriate")
    def flag(self, request, *args, **kwargs):
        flagger, article = self.request.user, self.get_object()
        flag, created = models.Flags.objects.get_or_create(flagger_id=flagger.id, article_id=article.id)
        if created is False:
            flag.delete()
        # return saved flagged/un-flagged article
        return Response(self.get_serializer(instance=self.get_object()).data)

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


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsOwnerOrSuperuserOrReadOnly]

    def perform_create(self, serializer):
        self.perform_update(serializer)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user, article_id=self.kwargs.get('article_id'), )

    def get_queryset(self):
        return models.Comments.objects.filter(article_id=self.kwargs.get('article_id'), )
