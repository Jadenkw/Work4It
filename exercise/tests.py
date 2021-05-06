from django.test import TestCase
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse

# Create your tests here.
class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_home_page_status_code(self):
        response = self.client.get('/leaderboard')
        self.assertEquals(response.status_code, 301)

    def test_home_page_status_code(self):
        response = self.client.get('/workout')
        self.assertEquals(response.status_code, 301)

    def test_home_page_status_code(self):
        response = self.client.get('/video')
        self.assertEquals(response.status_code, 301)