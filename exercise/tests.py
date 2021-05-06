from django.test import TestCase
from exercise.models import Item, Workout
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse
import datetime
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

class VideoTestCase(TestCase):
    def setUp(self):
        Item.objects.create(video="youtube.com", video_title="Title")
        Item.objects.create(video="youtube.com",video_title="Not Title")
    def test_video_title(self):
        """Test that videos have correctly assigned titles"""
        video1 = Item.objects.get(video_title="Title")
        video2 = Item.objects.get(video_title="Not Title")
        self.assertEqual(video1.video_title, "Title")
        self.assertEqual(video2.video_title, "Not Title")
        
class WorkoutTestCase(TestCase):
    def setUp(self):
        Workout.objects.create(workout_title="Sample", workout_pub_date = "2021-05-06", workout_calories=500, workout_description = "Description")
    def test_calorie_count(self):
        sampleworkout = Workout.objects.get(workout_title="Sample")
        self.assertEqual(sampleworkout.workout_calories, 500)