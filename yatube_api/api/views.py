from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.shortcuts import get_object_or_404

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)
from posts.models import Group, Post, User


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        new_queryset = get_object_or_404(Post, id=post_id)
        return new_queryset.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=self.kwargs.get('post_id'))
        )


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        new_queryset = get_object_or_404(User, username=self.request.user)
        return new_queryset.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
