from rest_framework import serializers
from questions.models import Question, Comment

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'question','body', 'created_at', 'updated_at','like_count', 'dislike_count']
        # liked_users and disliked users are not included. Just count of them is included. Further it can be change.
    
    def get_like_count(self, obj):
        return obj.like_count() # goes to model's function named like_count 

    def get_dislike_count(self, obj):
        return obj.dislike_count()


class QuestionSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)  # Nested serializer for comments

    class Meta:
        model = Question
        fields = ["id","user","title","body","created_at","updated_at","like_count","dislike_count","comments"]
        # liked_users and disliked users are not included. Just count of them is included. Further it can be change.
        
    def get_like_count(self, obj):
        return obj.like_count()

    def get_dislike_count(self, obj):
        return obj.dislike_count()
    

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'created_at', 'updated_at', 'liked_users', 'disliked_users']
        read_only_fields = ['created_at', 'updated_at', 'liked_users', 'disliked_users']
        

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','question','body','created_at','updated_at','liked_users', 'disliked_users']
        read_only_fields = ['created_at','updated_at','liked_users', 'disliked_users']