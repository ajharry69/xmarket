from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from article.models import Article


class TestArticle(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.author = get_user_model().objects.create_user(email='user@mail-domain.com', username='user123', )

    def test_article_to_str(self):
        article = Article.objects.create(author=self.author, headline='h1', content='c1', )
        self.assertEqual(article.__str__(), f'{article}')
        self.assertEqual(article.__str__(), f'h1')
