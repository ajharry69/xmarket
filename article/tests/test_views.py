from django.contrib.auth import get_user_model
from django.core.files import uploadedfile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestArticleViewSet(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.author = get_user_model().objects.create_user(email='user@mail-domain.com', username='user123', )

    def test_add_article_without_media(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.author.token.encrypted}')
        response = self.client.post(reverse('article-list'), data={
            'headline': 'h1',
            'content': 'c1',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_article_with_media(self):
        file1 = uploadedfile.SimpleUploadedFile('file.jpg', b'content', 'image/jpeg')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.author.token.encrypted}')
        response = self.client.post(reverse('article-list'), data={
            'media': file1.file,
            'article': {'headline': 'h1', 'content': 'c1', },
        }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
