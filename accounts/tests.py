from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.
class PasswordChangeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(first_name='trippier', last_name='kierian',
        	phone_number='09088899900', email='trippier@gmail.com',date_for_your_onboarding='26/05/2023',
        	 password='test_password')

    def test_password_change(self):
        # Authenticate the user
        self.client.login(phone_number='09088899900', password='test_password')

        # Simulate password change request
        response = self.client.post('/change-password/', {
            'old_password': 'test_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        })

        # Assert the expected response status code
        self.assertEqual(response.status_code, 404) 






