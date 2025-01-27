from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Video
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import VideoSerializer
from rest_framework.response import Response
from rest_framework import status

class VideoPostView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class = VideoSerializer
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            serializer.save(author=request.user)
            return Response({'msg':'Video Posted!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class VideoListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

class LikeVideoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(request, video_id):
        video = get_object_or_404(Video, id=video_id)
        user = request.user

        if user in video.disliked_by.all():
            video.disliked_by.remove(user)
            video.dislikes -= 1

        if user not in video.liked_by.all():
            video.liked_by.add(user)
            video.likes += 1
        else:
            video.liked_by.remove(user)
            video.likes -= 1
        video.save()
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DislikeVideoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(request, video_id):
        video = get_object_or_404(Video, id=video_id)
        user = request.user
        if user in video.liked_by.all():
            video.liked_by.remove(user)
            video.likes -= 1
        if user not in video.disliked_by.all():
            video.disliked_by.add(user)
            video.dislikes += 1
        else:
            video.disliked_by.remove(user)
            video.dislikes -= 1
        video.save()
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VideoModifyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoSerializer    
    def get(self, request, pk=None, format=None):
        id=pk
        if id is not None:
            try:
                post=Video.objects.get(id=id)
                serializer = VideoSerializer(post)
                return Response(serializer.data)
            except Video.DoesNotExist:
                return Response({"msg":"Video doesnot exist!"}, status=status.HTTP_404_NOT_FOUND)
                    
        post = Video.objects.all()
        serializer = VideoSerializer(post, many=True)
        return Response(serializer.data)
    
    def patch(self, request, pk=None, format=None):
        id=pk
        try:
            post = Video.objects.get(pk=id)
            if post.author != request.user:
                return Response({"msg":"You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN)
        except Video.DoesNotExist:
            return Response({"msg":"Video Does not Exist!"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = VideoSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Updated!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None, format=None):
        id=pk
        try:
            post = Video.objects.get(pk=id)
            if post.author != request.user:
                return Response({"msg":"You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN)
        except Video.DoesNotExist:
            return Response({"msg":"Post Does not Exist!"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = VideoSerializer(post, data=request.data,)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, format=None):
        id=pk
        try:
            post = Video.objects.get(pk=id)
            if post.author != request.user:
                return Response({"msg": "You do not have permission to delete this Video."}, status=status.HTTP_403_FORBIDDEN)
            post.delete()
            return Response({'msg':'Data Deleted!'})
        except Video.DoesNotExist:
            return Response({"msg":"Video doesnot exist!"}, status=status.HTTP_404_NOT_FOUND)