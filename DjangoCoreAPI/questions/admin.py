from django.contrib import admin
from questions.models import Question, Comment

admin.site.register(Question)
admin.site.register(Comment)