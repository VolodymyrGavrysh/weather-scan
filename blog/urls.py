from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)

from . import views
from apps.endpoints.urls import urlpatterns

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('price/', views.pricing, name='blog-pricing'),
    path('map/', views.show_plotly, name='map'),
    path('future/', views.show_plotly_future, name='future'),

    ]

    # UserPostListView
    # path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),


# http://127.0.0.1:8000/api/v1/income_classifier/predict
# path('api/v1/income_classifier/predict', PredictView.as_view(), name='api'),
