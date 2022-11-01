from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

# Create your tests here.
# class UserRegistrationAPIViewTestCase(APITestCase):
#     def test_registration(self):
#         url = reverse('user_view')
#         user_data = {
#             "email": "test@gmail.com",
#             "password": "password"
#         }
#         response = self.client.post(url, user_data)
#         self.assertEqual(response.status_code, 201)
    
#     def test_login(self):
#         url = reverse('token_obtain_pair')
#         user_data = {
#             "email": "test@gmail.com",
#             "password": "password"
#         }
#         response = self.client.post(url, user_data)
#         self.assertEqual(response.status_code, 200)


class LoginUserTest(APITestCase):
    def setUp(self):
        self.data = {'email':'kim@gmail.com', 'password':'kimpassword'}
        self.user = User.objects.create_user('kim@gmail.com', 'kimpassword')
    
    def test_login(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.get(
            path=reverse('mock_view'),
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)

# class LoginUserTest(APITestCase):
#     def setUp(self):
#         self.data = {"email":"kim@gmail.com", "password":"kimpassword"}
#         self.user = User.objects.create_user("kim@gmail.com", "kimpassword")

#     def test_login(self):
#         response = self.client.post(reverse('token_obtain_pair'), self.data)
#         self.assertEqual(response.status_code, 200)

#     def test_get_user_data(self):
#         access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
#         response = self.client.get(
#             path=reverse("mock_view"),
#             HTTP_AUTHORIZATION = f"Bearer {access_token}"
#         )
        
#         self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data['email'], self.data['email'])
        