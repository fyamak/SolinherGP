from django.urls import path
from .views import RAGSearchView

urlpatterns = [
    path("rag-search/", RAGSearchView.as_view(), name="rag_search"),
]
