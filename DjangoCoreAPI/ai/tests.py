from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
import time

CustomUser = get_user_model()

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", 
            password="Password123!",
            first_name="Test",
            last_name="User",
            role="employee"
        )
        print("# AI Time Measurement #")
        
    
    def test_performance_ai(self):
        """
        Test for measuring ai performance
        """
        query_data = {
            "query" : ""
        }
        self.client.force_authenticate(user=self.user)
        start = time.time()
        self.client.post(reverse("rag_search"),query_data)
        end = time.time() 
        print(f"AI training time: {(end-start):.5f} second")
        
        query_data["query"] = "Test question?"
        start = time.time()
        self.client.post(reverse("rag_search"),query_data)
        end = time.time() 
        print(f"AI answer time: {(end-start):.5f} second")