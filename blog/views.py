from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import PostSerializer
from .models import Post
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import ListAPIView

# from .filters import PostFilter
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

# Create your views here.
class BlogApi(ListAPIView):
    queryset = Post.objects.all()
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    filter_backends = [OrderingFilter]
    
class BlogPost(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    # filter_backends = [OrderingFilter]
    
    def post(self, request, pk=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({'msg':'Blog Posted!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BlogModify(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer    
    def get(self, request, pk=None, format=None):
        id=pk
        if id is not None:
            try:
                blog=Post.objects.get(id=id)
                serializer = PostSerializer(blog)
                return Response(serializer.data)
            except Post.DoesNotExist:
                return Response({"msg":"Post doesnot exist!"}, status=status.HTTP_404_NOT_FOUND)
                    
        blog = Post.objects.all()
        serializer = PostSerializer(blog, many=True)
        return Response(serializer.data)
    
    def patch(self, request, pk=None, format=None):
        id=pk
        try:
            blog = Post.objects.get(pk=id)
            if blog.author != request.user:
                return Response({"msg":"You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response({"msg":"Post Does not Exist!"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = PostSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Updated!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None, format=None):
        id=pk
        try:
            blog = Post.objects.get(pk=id)
            if blog.author != request.user:
                return Response({"msg":"You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response({"msg":"Post Does not Exist!"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = PostSerializer(blog, data=request.data,)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, format=None):
        id=pk
        try:
            blog = Post.objects.get(pk=id)
            if blog.author != request.user:
                return Response({"msg": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
            blog.delete()
            return Response({'msg':'Data Deleted!'})
        except Post.DoesNotExist:
            return Response({"msg":"Post doesnot exist!"}, status=status.HTTP_404_NOT_FOUND)