from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

app_name = 'api'

# version 1
router1 = DefaultRouter()
router1.register('posts', PostViewSet, basename='posts')
router1.register(
    r'posts/(?P<post_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments')
router1.register('groups', GroupViewSet, basename='groups')
router1.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
