from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from myapp.models import UserData
from django.core.cache import cache
import json
import pyotp

@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
})
class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.session_url = reverse('session')
        self.csrf_url = reverse('csrf') 
        
        self.user = UserData.objects.create(
            email="testuser@example.com",
            password=make_password("Password1234"),
            name="Test User",
            display_name="Tester",
            role=1,
            mfa_secret=pyotp.random_base32()
        )
        cache.clear()

    def get_csrf_token(self):
        """ Helper function to get CSRF token """
        csrf_response = self.client.get(self.csrf_url)
        return csrf_response.json().get("csrf_token")

    def test_login_success(self):
        csrf_token = self.get_csrf_token()
        totp = pyotp.TOTP(self.user.mfa_secret).now()
        payload = {
            "username": "testuser@example.com",
            "password": "Password1234",
            "mfa_code": totp
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token  
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Logged in successfully")

    def test_login_invalid_username(self):
        csrf_token = self.get_csrf_token()
        totp = pyotp.TOTP(self.user.mfa_secret).now()
        payload = {
            "username": "nonexistent@example.com",
            "password": "Password1234",
            "mfa_code": totp
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid credentials")

    def test_login_invalid_password(self):
        csrf_token = self.get_csrf_token()
        totp = pyotp.TOTP(self.user.mfa_secret).now()
        payload = {
            "username": "testuser@example.com",
            "password": "WrongPassword",
            "mfa_code": totp
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid credentials")

    def test_login_invalid_mfa_code(self):
        csrf_token = self.get_csrf_token()
        payload = {
            "username": "testuser@example.com",
            "password": "Password1234",
            "mfa_code": "000000"  # Invalid MFA code
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid MFA code")

    def test_login_rate_limit_exceeded(self):
        csrf_token = self.get_csrf_token()
        totp = pyotp.TOTP(self.user.mfa_secret).now()
        payload = {
            "username": "testuser@example.com",
            "password": "WrongPassword",
            "mfa_code": totp
        }
        for _ in range(5):
            response = self.client.post(
                self.login_url,
                data=json.dumps(payload),
                content_type='application/json',
                HTTP_X_CSRFTOKEN=csrf_token
            )
        # The sixth attempt should trigger rate limit
        response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token
        )
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.json()["error"], "Too many failed login attempts. Please try again in 10 minutes.")

    def test_login_missing_fields(self):
        csrf_token = self.get_csrf_token()
        payload = {
            "username": "testuser@example.com",
            # Missing "password" field
            "mfa_code": "123456"
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Username and password required")

    def test_register_success(self):
        csrf_token = self.get_csrf_token()
        payload = {
            "username": "newuser@example.com",
            "password": "NewPassword123",
            "name": "New User",
            "displayname": "NewUser"
        }
        response = self.client.post(
            self.register_url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "User registered successfully")

    def test_register_username_already_exists(self):
        csrf_token = self.get_csrf_token()
        payload = {
            "username": "testuser@example.com",  # Existing username
            "password": "NewPassword123",
            "name": "Test User",
            "displayname": "TestUser"
        }
        response = self.client.post(
            self.register_url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Username already exists")

    def test_register_invalid_password_format(self):
        csrf_token = self.get_csrf_token()
        payload = {
            "username": "anotheruser@example.com",
            "password": "short",  # Invalid password
            "name": "Another User",
            "displayname": "AnotherUser"
        }
        response = self.client.post(
            self.register_url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "invalidPassword")

    def test_session_view_unauthenticated(self):
        response = self.client.get(self.session_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "No session ID found in cookies")

    def test_logout_success(self):
        csrf_token = self.get_csrf_token()
        # Log in the user to establish a session
        totp = pyotp.TOTP(self.user.mfa_secret).now()
        login_payload = {
            "username": "testuser@example.com",
            "password": "Password1234",
            "mfa_code": totp
        }
        self.client.post(
            self.login_url,
            data=json.dumps(login_payload),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token
        )
        
        # Test logout
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Logged out successfully")
