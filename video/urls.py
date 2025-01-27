from django.urls import path
from . import views

urlpatterns = [
    path('service/', views.VideoListAPIView.as_view(), name='video_list'),
    path('postvideo/', views.VideoPostView.as_view(), name='video_post'),
    path('modifyvideo/<int:pk>/', views.VideoModifyView.as_view(), name='modify_video'),
    path('like/<int:video_id>/', views.LikeVideoAPIView.as_view(), name='like_video'),
    path('dislike/<int:video_id>/', views.DislikeVideoAPIView.as_view(), name='dislike_video'),    
]