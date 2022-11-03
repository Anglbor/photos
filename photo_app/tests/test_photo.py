from django.test import TestCase
from django.contrib.auth.models import User

from photo_app.models import Photo

class PhotoTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="54321")
        pass

    def test_photo_default(self):
        # Create a photo and check default values are as expected.
        photo = Photo.objects.create(photo=None, sender=self.user)
        self.assertEqual(photo.name, "blank")
