from rest_framework import viewsets, filters
# from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from posts.models import Follow, Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer
from .serializers import CommentSerializer, FollowSerializer
from .permissions import OwnerOrReadOnly, OwnerOnly
from django.contrib.auth import get_user_model
from .pagination import PostsPagination

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [OwnerOrReadOnly]
    pagination_class = PostsPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [OwnerOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [OwnerOrReadOnly]

    def get_queryset(self):
        # Получаем id post из эндпоинта
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        # И отбираем только нужные комментарии
        new_queryset = Comment.objects.filter(post=post)
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [OwnerOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        new_queryset = Follow.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
