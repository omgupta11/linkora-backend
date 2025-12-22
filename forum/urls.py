from django.urls import path
from .views import PostListCreateView, CommentCreateView

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("<int:post_id>/comment/", CommentCreateView.as_view()),
]
