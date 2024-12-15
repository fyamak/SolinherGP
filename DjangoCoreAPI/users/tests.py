from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

CustomUser = get_user_model()

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'employee',
            'receive_email_notifications': True
        }
        self.user = CustomUser.objects.create_user(
            email=self.user_data['email'], 
            password=self.user_data['password'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            role=self.user_data['role'],
            receive_email_notifications = self.user_data['receive_email_notifications']
        )
        

    def test_user_registration_success(self):
        """
        Test for successfull user registration
        """
        user_data = {
            'email': 'testuser2@example.com',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'first_name': 'Test2',
            'last_name': 'User',
            'role': 'hr',
            'receive_email_notifications': True
        }
        response = self.client.post(reverse('register') , user_data)
        
        self.assertEqual(user_data['password'], user_data['password2'], 'Password does not match')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Expected status code not returned')

    
    def test_user_registration_fail(self):
        """
        Test for unsuccessfull user registration
        """
        response = self.client.post(reverse('register') , self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'User with this email is already exists. Expected status code not returned.')
        

    def test_user_login_success(self):
        """
        Test for successfull user login
        """
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK , 'Login failed even though login information is valid.')
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        

    def test_user_login_failure(self):
        """
        Test for login with incorrect credentials
        """
        login_data = {
            'email': self.user_data['email'],
            'password': 'WrongPassword'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        

    def test_retrieve_user_profile(self):
        """
        Test for retrieving authenticated user's profile
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user_detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response.data['id'], self.user.id, "ID field does not match.")
        self.assertEqual(response.data['email'], self.user.email, "Email field does not match.")
        self.assertEqual(response.data['first_name'], self.user.first_name, "First name field does not match.")
        self.assertEqual(response.data['last_name'], self.user.last_name, "Last name field does not match.")
        self.assertEqual(response.data['role'], self.user.role, "Role field does not match.")
    

    def test_update_user_profile(self):
        """
        Test for updating user profile
        """
        self.client.force_authenticate(user=self.user)
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'role': 'manager',
            'receive_email_notifications': False
        }
        response = self.client.put(reverse('user_update'), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        
        updated_user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.first_name, update_data["first_name"], 'First name field is not updated.')
        self.assertEqual(updated_user.last_name, update_data["last_name"], 'Last name field is not updated.')
        self.assertEqual(updated_user.role, update_data["role"], 'Role field is not updated.')
        self.assertFalse(updated_user.receive_email_notifications, 'Receive email notification field is not updated.')


    def test_change_password(self):
        """
        Test for changing user password
        """
        self.client.force_authenticate(user=self.user)
        change_password_data = {
            'old_password': self.user_data['password'],
            'new_password': 'NewPassword123!',
            'new_password2': 'NewPassword123!'
        }
        response = self.client.post(reverse('change_password'), change_password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')

        login_data = {
            'email': self.user_data['email'],
            'password': change_password_data['new_password']
        }
        login_response = self.client.post(reverse('login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK, 'Expected status code not returned')


    def test_delete_user(self):
        """
        Test for user account deletion
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('user_delete'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Expected status code not returned')
        
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(pk=self.user.pk)
    

    def test_get_user_by_id(self):
        """
        Test for retrieving a user by their ID
        """
        get_user_url = reverse('get-user-by-id', kwargs={'pk': self.user.pk})
        response = self.client.get(get_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response.data['email'], self.user.email, 'Email field does not match.')