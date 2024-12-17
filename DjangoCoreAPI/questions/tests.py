from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Question,Comment,Tag

CustomUser = get_user_model()

# Create your tests here.
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
        self.tag1 = Tag.objects.create(name="tag1")
        self.tag2 = Tag.objects.create(name="tag2")
        self.question = Question.objects.create(
            title="test question",
            body="test body",
            user=self.user
        )
        # adding tag to created question because we cannot add an object to ManyToManyField when we creating an instance
        self.question.tags.add(self.tag1,self.tag2)
        self.comment = Comment.objects.create(
            user = self.user,
            question = self.question,
            body = "test comment body"
        )
        
    
    def test_create_question_successfully(self):
        """
        Test for creating question successfully
        """
        question_data = {
            "title" : "Test creating question",
            "body" : "content",
            "tags" : []
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("create_question"),question_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Expected status code not returned')

    
    def test_create_question_unsuccessfully(self):
        """
        Test for creating question unsuccessfully
        """
        invalid_question_data = {
            "title" : "Test creating question",
            "tags" : ["test","tags","question"]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("create_question"),invalid_question_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, f'Expected status code not returned')
    
    
    def test_create_comment_successfully(self):
        """
        Test for creating comment successfully
        """
        comment_data = {
            "question" : self.question.id,
            "body" : "Test body content for test.",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("create_comment"), comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Expected status code not returned')
    
    
    def test_create_comment_unsuccessfully(self):
        """
        Test for creating comment unsuccessfully
        """
        comment_data = {
            "body" : "Test body content for test.",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("create_comment"), comment_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Expected status code not returned')
    
    
    def test_own_questions(self):
        """
        Test for users' own question
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('own_questions'))
        for x in response.data:
            self.assertEqual(x["user"], self.user.id)
    
    
    def test_search_question(self):
        """
        Test for searching by string in questions
        """
        search_string = "test"
        response = self.client.get(reverse("search"), {'search':search_string})

        for rd in response.data:
            is_found = False
            user_response = self.client.get(reverse('get-user-by-id', kwargs={'pk': rd["user"]}))
            if (
                search_string.lower() in rd['title'].lower() or 
                search_string.lower() in rd['body'].lower()
            ):
                is_found = True
            elif(
                search_string.lower() in user_response['first_name'].lower() or
                search_string.lower() in user_response['last_name'].lower()
            ):
                is_found = True
            self.assertTrue(is_found,"Question was returned even though the searched word was not in the question.")
       

        search_tag = "tag1"
        response_tag = self.client.get(reverse("search"), {'tags__name':search_tag})
        
        for rd in response_tag.data:
            is_found = False
            if (search_tag in rd["tag_names"]):
                is_found = True
            self.assertTrue(is_found,"Question was returned even though the tag was not in the question's tag.")
            
    
    def test_edit_question(self):
        """
        Test for editing questions
        """
        update_data = {
            "title" : "Updated title",
            "body" : "Updated body",
            "tags" : ["updatedTag1", "updatedTag2"]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse("edit-question", kwargs={"pk": self.question.id}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response.data["title"], update_data["title"], "Updated title does not appear.")
        self.assertEqual(response.data["body"], update_data["body"], "Updated body does not appear")
        self.assertEqual(set(response.data["tag_names"]), set(update_data["tags"]), "Updated tags does not appear")
    
    
    def test_edit_comment(self):
        """
        Test for editing comments
        """
        update_data = {
            "body" : "Updated body"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse("edit-comment", kwargs={"pk": self.comment.id}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response.data["body"], update_data["body"], "Updated body does not appear")
        
    
    def test_get_question_by_id(self):
        """
        Test for getting question by id
        """
        response = self.client.get(reverse("question", kwargs={"pk":self.question.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response.data["id"], self.question.id, "Question's ID does not match.")

    
    def test_like_question(self):
        """
        Test to like and unlike question 
        """
        # Like
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("like_question", kwargs={"pk":self.question.id}))
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response_question.data["like_count"], 1, "Question is not liked successfully.")
        
        # Unlike
        response = self.client.post(reverse("like_question", kwargs={"pk":self.question.id}))
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response_question.data["like_count"], 0, "Question is not unliked successfully.")
        
        
    def test_dislike_question(self):
        """
        Test to dislike and undislike question 
        """
        # dislike
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("dislike_question", kwargs={"pk":self.question.id}))
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response_question.data["dislike_count"], 1, "Question is not disliked successfully.")
        
        # Undislike
        response = self.client.post(reverse("dislike_question", kwargs={"pk":self.question.id}))
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response_question.data["dislike_count"], 0, "Question is not undisliked successfully.")
        
    
    def test_like_comment(self):
        """
        Test to like and unlike comment 
        """
        # Like
        self.client.force_authenticate(user=self.user)
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id})) # for taking question's first comment id
        response = self.client.post(reverse("like_comment", kwargs={"pk":response_question.data["comments"][0]["id"]}))
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id})) # For asserting
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response_question.data["comments"][0]["like_count"], 1, "Comment is not liked successfully.")

        # Unlike
        response = self.client.post(reverse("like_comment", kwargs={"pk":response_question.data["comments"][0]["id"]}))
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id})) # For asserting

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response_question.data["comments"][0]["like_count"], 0, "Comment is not unliked successfully.")


    def test_dislike_comment(self):
        """
        Test to dislike and undislike comment 
        """
        # dislike
        self.client.force_authenticate(user=self.user)
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id})) # for taking question's first comment id
        response = self.client.post(reverse("dislike_comment", kwargs={"pk":response_question.data["comments"][0]["id"]}))
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id})) # For asserting
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response_question.data["comments"][0]["dislike_count"], 1, "Comment is not disliked successfully.")
        
        # Undislike
        response = self.client.post(reverse("dislike_comment", kwargs={"pk":response_question.data["comments"][0]["id"]}))
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id})) # For asserting

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertEqual(response_question.data["comments"][0]["dislike_count"], 0, "Comment is not undisliked successfully.")

    
    def test_favorite_question(self):
        """
        Test for favorite question
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("favorite_question", kwargs={"pk":self.question.id}))
        response_question = self.client.get(reverse("question", kwargs={"pk":self.question.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected status code not returned')
        self.assertIn(self.user.id, response_question.data["favorited_by"], "User's favorite is not found in question")