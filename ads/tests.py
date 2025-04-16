from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ads.models import Ad, Comment
from users.models import User


class AdsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.ad = Ad.objects.create(
            author=self.user,
            title="Продаю велосипед",
            description="Почти новый, не битый",
            price=15000,
        )
        self.client.force_authenticate(user=self.user)

    def test_ad_retrieve(self):
        url = reverse("ads:ad-detail", args=[self.ad.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.ad.title)

    def test_ad_create(self):
        url = reverse("ads:ad-list")
        data = {
            "title": "Новый ноутбук",
            "description": "Мощный и стильный",
            "price": 70000,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 2)

    def test_ad_update(self):
        url = reverse("ads:ad-detail", args=[self.ad.pk])
        data = {"price": 12000}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ad.objects.get(pk=self.ad.pk).price, 12000)

    def test_ad_delete(self):
        url = reverse("ads:ad-detail", args=[self.ad.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 0)

    def test_ad_list(self):
        url = reverse("ads:ad-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.ad = Ad.objects.create(
            author=self.user, title="Смартфон", description="Почти новый", price=20000
        )
        self.comment = Comment.objects.create(
            ad=self.ad, author=self.user, text="Отличное объявление!"
        )
        self.client.force_authenticate(user=self.user)

    def test_comment_list(self):
        url = reverse("ads:comment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_comment_create(self):
        url = reverse("ads:comment-list")
        data = {"ad": self.ad.id, "text": "Интересует, можно скидку?"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_comment_retrieve(self):
        url = reverse("ads:comment-detail", args=[self.comment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], self.comment.text)

    def test_comment_update(self):
        url = reverse("ads:comment-detail", args=[self.comment.pk])
        data = {"text": "Обновлённый комментарий"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, "Обновлённый комментарий")

    def test_comment_delete(self):
        url = reverse("ads:comment-detail", args=[self.comment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())
