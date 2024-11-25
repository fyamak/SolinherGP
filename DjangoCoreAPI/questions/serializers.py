from rest_framework import serializers
from questions.models import Question, Comment, Tag

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'question','body', 'created_at', 'updated_at','like_count', 'dislike_count']
        read_only_fields = ['user','created_at','updated_at','liked_users', 'disliked_users']
        # liked_users and disliked users are not included. Just count of them is included. Further it can be change.
    
    def get_like_count(self, obj):
        return obj.like_count() # goes to model's function named like_count 

    def get_dislike_count(self, obj):
        return obj.dislike_count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]  # Etiketlerle ilgili alanlar
        

class QuestionSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)  # Nested serializer for comments
    tags = serializers.ListField(child=serializers.CharField(max_length=50), write_only=True) # Every tag should be string, Write will only be used while POST request
    tag_names = serializers.SerializerMethodField() # For GET request
    
    class Meta:
        model = Question
        fields = ["id","user","title","body","tags","tag_names","created_at","updated_at","like_count","dislike_count","comments"]
        read_only_fields = ['user','created_at', 'updated_at', 'liked_users', 'disliked_users']
        # liked_users and disliked users are not included. Just count of them is included. Further it can be change.
        
    def create(self, validated_data):
        tags = validated_data.pop("tags", [])  # Extract tags into list
        question = Question.objects.create(**validated_data)

        for tag_name in set(tags):  # Same tag filter
            tag, created = Tag.objects.get_or_create(name=tag_name)
            question.tags.add(tag)
        return question
    
    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]
                
    def get_like_count(self, obj):
        return obj.like_count()

    def get_dislike_count(self, obj):
        return obj.dislike_count()