from django.apps import AppConfig


class ArticleConfig(AppConfig):
    name = 'article'

    # noinspection PyUnresolvedReferences
    def ready(self):
        from article import signals
