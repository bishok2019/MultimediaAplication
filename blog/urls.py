from django.urls import path
from . import views

urlpatterns =[
    path('blogapi/', views.BlogApi.as_view()),
    path('blogpost/', views.BlogPost.as_view()),
    path('blogmodify/<int:pk>', views.BlogModify.as_view()),
    # path('blogmodify/', views.BlogModify.as_view()),
]
