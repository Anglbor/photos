from django.test import TestCase
from django.contrib.auth.models import User

class TestLogin(TestCase):
    ''' A simple login test class, with a single login test case.
    Make sure the test database can be created with the appropriate django
    user from settings.py with the following:
    ALTER USER <user> CREATEDB;
    '''

    @classmethod
    def setUpClass(cls):
        cls.password = 'MyPassword2023'
        cls.username = 'testuser'

        # Create a test user. Django will automatically remove this user
        # when the test class is finished.
        user = User.objects.create(username=cls.username)
        user.set_password(cls.password)
        user.save()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_00_login(self):
        ''' Test that a simple user can be logged in.
        '''
        body = {
            'username': self.username,
            'password': self.password
        }
        # Need to set follow=True so that redirects are followed.
        response = self.client.post('/login/', body, follow=True)
        self.assertEqual(200, response.status_code)
