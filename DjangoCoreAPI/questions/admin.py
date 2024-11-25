from django.contrib import admin
from questions.models import Question, Comment,Tag

admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Tag)