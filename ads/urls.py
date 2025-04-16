from django.urls import path

from ads.views import (
    AdListCreateView,
    AdRetrieveUpdateDestroyView,
    CommentListCreateView,
    CommentRetrieveUpdateDestroyView,
)

app_name = "ads"

urlpatterns = [
    path("", AdListCreateView.as_view(), name="ad-list"),
    path("<int:pk>/", AdRetrieveUpdateDestroyView.as_view(), name="ad-detail"),
    path("comments/", CommentListCreateView.as_view(), name="comment-list"),
    path(
        "comments/<int:pk>/",
        CommentRetrieveUpdateDestroyView.as_view(),
        name="comment-detail",
    ),
]
