from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ...models import Post
from accounts.models import Profile
from .serializer import PostSerializer
from .permission import IsOwnerOrReadOnly
from .serializer import PostSerializer
from .filters import PostFilters
from .paginations import DefaultPagination

# this variable is used fro user model
User = get_user_model()


# this viewset is similar to APIView which for any method request, you can use one function
# in viewset, default permission_classes is is_authenticated
class PostViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    # Action to create a new book
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ModelViewSet is combine of model serializer and ViewSet
# ypu can send Html from model database
class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.filter(status=True)
    serializer_class = PostSerializer
    filter_backends = [OrderingFilter]
    filterset_class = PostFilters
    search_fields = ["title", "body"]
    ordering_fields = ["created_date"]


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=True)
    serializer_class = PostSerializer
    pagination_class = DefaultPagination
    permission_classes = [AllowAny]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Post.objects.filter(status=True)
