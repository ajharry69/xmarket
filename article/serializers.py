import json

from rest_framework import serializers

from article import models
from user.serializers.profile import PublicProfileSerializer


class ArticleMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = ('content',)

    def to_representation(self, instance):
        return f'{self.get_media_url(instance)}'

    def get_media_url(self, media):
        url = None
        try:
            url = self.context.get('request').build_absolute_uri(media.content.url)
        finally:
            return url


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = PublicProfileSerializer(read_only=True)
    publication_date = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    media_urls = ArticleMediaSerializer(source='media_set',
                                        many=True, read_only=True, allow_null=True, default=None, )

    class Meta:
        model = models.Article
        fields = ('url', 'id', 'headline', 'content', 'publication_date', 'author', 'media_urls',)
        read_only_fields = ('id',)


class ArticleRequestSerializer(serializers.Serializer):
    article = ArticleSerializer()
    media = serializers.ListField(child=serializers.FileField(), required=False, allow_null=True, default=None)

    def update(self, instance, validated_data):
        return self.save_article(validated_data, instance)

    def create(self, validated_data):
        return self.save_article(validated_data)

    def to_representation(self, instance):
        return instance

    def save_article(self, data, instance=None):
        media, article = data.get('media'), data.get('article') or data
        article = json.loads(article) if isinstance(article, (str, bytes)) else article
        article_serializer = ArticleSerializer(instance=instance, data=article, context=self.context)
        if article_serializer.is_valid(raise_exception=True):
            article = article_serializer.save(author=self.context.get('request').user)
            for medium in media or []:
                models.Media.objects.create(article=article, content=medium)

        return article_serializer.data
