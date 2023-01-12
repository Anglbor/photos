from django.test import TestCase
from django.contrib.auth.models import User

from photo_app.models import Photo, Tag

class PhotoTests(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(tag_name="Door")
        self.user = User.objects.create_user(username="tester", password="54321")
        pass

    def test_photo_default(self):
        # Create a photo and check default values are as expected.
        photo = Photo.objects.create(photo=None, sender=self.user)
        self.assertEqual(photo.name, "blank")

    def test_photo_name(self):
        photo = Photo.objects.create(name="Boby", photo=None, sender=self.user)
        self.assertEqual(photo.name, "Boby")

    def test_photo_tag(self):
        photo = Photo.objects.create(name="Boby", photo=None, sender=self.user)
        self.assertEqual(photo.name, "Boby")
        photo.tag.add(self.tag)
        self.assertEqual(1, photo.tag.all().count())
        self.assertEqual("Door", photo.tag.all()[0].tag_name)
