from django.db import models
from django.conf import settings  # To reference the User model


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="questions",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_questions', blank=True)
    disliked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_questions', blank=True)

    def like_count(self):
        return self.liked_users.count()

    def dislike_count(self):
        return self.disliked_users.count()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.title}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    disliked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_comments', blank=True)

    def like_count(self):
        return self.liked_users.count()

    def dislike_count(self):
        return self.disliked_users.count()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.question.title}'
