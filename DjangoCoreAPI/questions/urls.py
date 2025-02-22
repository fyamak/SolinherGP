from django.urls import path
from questions.views import (
    AllQuestions, AllTags, CreateQuestion, CreateComment, OwnQuestions, FavoritedQuestions, Search,
    EditQuestion,EditComment, QuestionByID,
    LikeQuestion, DislikeQuestion, LikeComment, DislikeComment,
    FavoriteQuestion,
)

urlpatterns = [
    path("all-questions/", AllQuestions.as_view(), name="all_question"),
    path("all-tags/", AllTags.as_view(), name="all_tags"),
    path("create-question/",CreateQuestion.as_view(),name="create_question"),
    path("create-comment/",CreateComment.as_view(),name="create_comment"),
    path("own-questions/",OwnQuestions.as_view(),name="own_questions"),
    path("favorited-questions/",FavoritedQuestions.as_view(),name="favorited_questions"),
    path("search/", Search.as_view(),name="search"),
    path('edit-question/<int:pk>', EditQuestion.as_view(), name='edit-question'),
    path('edit-comment/<int:pk>', EditComment.as_view(), name='edit-comment'),
    path("question/<int:pk>", QuestionByID.as_view(), name="question"),
    path("like-question/<int:pk>", LikeQuestion.as_view(), name="like_question"),
    path("dislike-question/<int:pk>", DislikeQuestion.as_view(), name="dislike_question"),
    path("like-comment/<int:pk>", LikeComment.as_view(), name="like_comment"),
    path("dislike-comment/<int:pk>", DislikeComment.as_view(), name="dislike_comment"),
    path("favorite-question/<int:pk>", FavoriteQuestion.as_view(), name="favorite_question"),
]
