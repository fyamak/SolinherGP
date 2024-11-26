from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.generics import get_object_or_404
from questions.models import Question, Comment
from questions.serializers import QuestionSerializer, CommentSerializer
from drf_yasg.utils import swagger_auto_schema


class ListQuestionView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        responses={200: QuestionSerializer()}
    )
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CreateQuestion(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=QuestionSerializer,
        responses={200: 'Question successfully created', 400: 'Question not created'}
    )
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateComment(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={
            200: "Comment successfully created",
            400: "Comment not created",
        }
    )
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
            
    
class LikeQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        
        if request.user in question.disliked_users.all():
            question.disliked_users.remove(request.user)  # Remove from dislikes if already disliked
            
        if request.user in question.liked_users.all():
            question.liked_users.remove(request.user)  # Toggle like off
            return Response({"message": "Like removed"}, status=status.HTTP_200_OK)
        else:
            question.liked_users.add(request.user)  # Add like
            return Response({"message": "Liked successfully"}, status=status.HTTP_200_OK)
        

class DislikeQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        
        if request.user in question.liked_users.all():
            question.liked_users.remove(request.user)  # Remove from likes if already liked,
            
        if request.user in question.disliked_users.all():
            question.disliked_users.remove(request.user)  # Toggle dislike off 
            return Response({"message": "Dislike removed"}, status=status.HTTP_200_OK)
        else:
            question.disliked_users.add(request.user)  # Add dislike
            return Response({"message": "Disliked successfully"}, status=status.HTTP_200_OK)
        

class LikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        
        if request.user in comment.disliked_users.all():
            comment.disliked_users.remove(request.user)  # Remove from dislikes if already disliked
            
        if request.user in comment.liked_users.all():
            comment.liked_users.remove(request.user)  # Toggle like off
            return Response({"message": "Like removed"}, status=status.HTTP_200_OK)
        else:
            comment.liked_users.add(request.user)  # Add like
            return Response({"message": "Liked successfully"}, status=status.HTTP_200_OK)
        

class DislikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        
        if request.user in comment.liked_users.all():
            comment.liked_users.remove(request.user)  # Remove from likes if already liked,
            
        if request.user in comment.disliked_users.all():
            comment.disliked_users.remove(request.user)  # Toggle dislike off 
            return Response({"message": "Dislike removed"}, status=status.HTTP_200_OK)
        else:
            comment.disliked_users.add(request.user)  # Add dislike
            return Response({"message": "Disliked successfully"}, status=status.HTTP_200_OK)


class FavoriteQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        if request.user in question.favorited_by.all():
            question.favorited_by.remove(request.user)
            return Response({"message": "Removed from favorites"}, status=status.HTTP_200_OK)
        else:
            question.favorited_by.add(request.user)
            return Response({"message": "Added to favorites"}, status=status.HTTP_200_OK)