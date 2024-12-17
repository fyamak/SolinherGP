from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework import filters
from questions.models import Question, Comment
from questions.serializers import QuestionSerializer, CommentSerializer
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend


class AllQuestions(APIView):
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
            201: "Comment successfully created",
            400: "Comment not created",
        }
    )
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
      

class OwnQuestions(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={200: QuestionSerializer()}
    )
    def get(self,request):
        own_questions = Question.objects.filter(user=request.user)
        serializer = QuestionSerializer(own_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# https://www.django-rest-framework.org/api-guide/filtering/#searchfilter
# https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
# optionally order filter can be added
# optionally flexible search for spelling can be added 
class Search(ListAPIView):
    permission_classes = [AllowAny]
    
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend] # Contains search (Default)
    # ManyToManyField with the lookup API double-underscore notation
    search_fields = ['user__first_name','user__last_name','title', 'body'] # /?search=anystring
    filterset_fields = ['tags__name'] # /?tags__name=tagstring
    


class EditQuestion(APIView):
    permission_classes = [IsAuthenticated]
    
    swagger_auto_schema(
        request_body=QuestionSerializer,
        responses={200: QuestionSerializer()}
    )
    def patch(self, request, pk):
        question = get_object_or_404(Question,pk=pk)
        
        if question.user != request.user:
            return Response({"error": "You are not allowed to edit this question."}, status=status.HTTP_403_FORBIDDEN)

        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditComment(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={200: CommentSerializer()}
    )
    def patch(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
    
        if comment.user != request.user:
            return Response({"error": "You are not allowed to edit this question."}, status=status.HTTP_403_FORBIDDEN)
        
        request_data = request.data.copy()
        if 'question' in request_data: # block to change question
            request_data.pop('question')
            
        serializer = CommentSerializer(comment, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class QuestionByID(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        responses={200: QuestionSerializer()}
    )
    def get(self,request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class LikeQuestion(APIView):
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
        

class DislikeQuestion(APIView):
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
        

class LikeComment(APIView):
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
        

class DislikeComment(APIView):
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


class FavoriteQuestion(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        if request.user in question.favorited_by.all():
            question.favorited_by.remove(request.user)
            return Response({"message": "Removed from favorites"}, status=status.HTTP_200_OK)
        else:
            question.favorited_by.add(request.user)
            return Response({"message": "Added to favorites"}, status=status.HTTP_200_OK)