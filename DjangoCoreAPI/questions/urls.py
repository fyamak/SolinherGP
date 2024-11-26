from django.urls import path
from questions.views import (
    ListQuestionView, CreateQuestion, CreateComment, OwnQuestions,
    LikeQuestionView, DislikeQuestionView, LikeCommentView, DislikeCommentView,
    FavoriteQuestionView,
)

# try these urls - they have never been tried 
urlpatterns = [
    path("list-questions/", ListQuestionView.as_view(), name="list_question"),
    path("create-question/",CreateQuestion.as_view(),name="create_question"),
    path("create-comment/",CreateComment.as_view(),name="create_comment"),
    path("own-questions/",OwnQuestions.as_view(),name="own_questions"),
    path("like-question/<int:pk>", LikeQuestionView.as_view(), name="like_question"),
    path("dislike-question/<int:pk>", DislikeQuestionView.as_view(), name="dislike_question"),
    path("like-comment/<int:pk>", LikeCommentView.as_view(), name="like_comment"),
    path("dislike-comment/<int:pk>", DislikeCommentView.as_view(), name="dislike_comment"),
    path("favorite-question/<int:pk>", FavoriteQuestionView.as_view(), name="favorite_question"),
]
