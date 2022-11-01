from rest_framework import response
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from articles import serializers
from users.models import User
from articles.models import Article
from faker import Faker
import pprint

# Create your tests here.

from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

# 임시 이미지 만듦
def get_temporary_image(temp_file):
    size = (200,200)
    color = (255,0,0,0)
    image = Image.new("RGBA",size, color)
    image.save(temp_file, 'png')
    return temp_file


class ArticleCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'email':'kim@gmail.com', 'password':'kimpassword'}
        cls.article_data = {'title':'some title', 'content':'some content'}
        cls.user = User.objects.create_user('kim@gmail.com', 'kimpassword')
        
    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
    
    def test_fail_if_not_logged_in(self):
        url = reverse('article_view')
        response = self.client.post(url, self.article_data)
        self.assertEqual(response.status_code, 401)

    def test_create_article(self):
        response = self.client.post(
            path=reverse('article_view'),
            data=self.article_data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 200)

    def test_create_article_with_image(self):
        # 임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile() # 이름이 있는 임시 파일 생성
        temp_file.name = 'image.png' # 임시 파일의 이름은 image.png
        image_file = get_temporary_image(temp_file) # 위에서 만든 임시 이미지를 temp_file에 넣음
        image_file.seek(0) # 이미지의 첫번째 프레임 받아옴
        self.article_data['image'] = image_file # 위에서 만든 이미지 파일을 데이터에 넣음

        # 이미지 post
        response = self.client.post(
            path=reverse('article_view'),
            data=encode_multipart(data= self.article_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 200)

class ArticleReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.articles = []
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.email(), cls.faker.word())
            cls.articles.append(Article.objects.create(user=cls.user, title=cls.faker.sentence(), content=cls.faker.text()))
    
    def test_get_article(self):
        for article in self.articles:
            url = article.get_absolute_url()
            response = self.client.get(url)
            serializer = serializers.ArticleSerializer(article).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)
                print(key, value)

    # def setUp(self):
    #     self.user_data = {'username':'kim', 'password':'kimpassword'}
    #     self.article_data = {'title':'some title', 'content':'some content'}
    #     self.user = User.objects.create_user('kim','kimpassword')
    #     self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']