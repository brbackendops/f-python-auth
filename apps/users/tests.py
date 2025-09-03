from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse

# rest_framework testcase
from rest_framework.test import APITestCase
from rest_framework import status


class UserTestCase(TestCase):
    
    def setUp(self):
        self.User = get_user_model()
        self.email = 'test@mail.com'
        self.password = 'test123'
        self.first_name = 'test'
        self.last_name = 'falcon'
        self.username = 'test falcon'
        
    def test_create_user(self):
        user = self.User.objects.create_user(email=self.email,password=self.password,first_name=self.first_name,last_name=self.last_name)
        
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(email=self.email,password=self.password,first_name='',last_name='')
    
    def test_create_superuser(self):
        user = self.User.objects.create_superuser(email=self.email,password=self.password,first_name=self.first_name,last_name=self.last_name)
        
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)
        
        with self.assertRaises(IntegrityError):
            self.User.objects.create_superuser(email=self.email,password=self.password,first_name='',last_name='')

class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.email = 'test@mail.com'
        self.password = 'test123'
        self.first_name = 'test'
        self.last_name = 'falcon'
        self.username = 'test falcon'                
    
    
    def test_signup_endpoint(self):
        url = reverse('user-signup')
        
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
        }
        
        res = self.client.post(url,data,format='json')
        
        self.assertEqual(res.headers['Content-Type'],'application/json')
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertIn("id",res.data['data'])
        self.assertIn("email",res.data['data'])
        self.assertIn("name",res.data['data'])
        self.assertIn("created_at",res.data['data'])
        
    def test_login_endpoint(self):
        
        self.user_model.objects.create_user(email=self.email,password=self.password,first_name=self.first_name,last_name=self.last_name)        
        
        url = reverse('user-login')
        
        data = {
            "email": self.email,
            "password": self.password
        }
        
        res = self.client.post(url,data,format='json')
        
        self.assertEqual(res.headers['Content-Type'],'application/json')
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn("token", res.data)
