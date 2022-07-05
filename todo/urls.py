from django.urls import path
from rest_framework.authtoken import views as views_token

from . import views

urlpatterns = [
    path('todo/', views.NoteListCreateApiView.as_view()),
    path('todo/<int:pk>/', views.NoteDetailApiView.as_view()),
    path('comments/', views.CommentListApiView.as_view()),
    path('todo/filters/', views.ToDoFilterListApiView.as_view()),
    path('comments/filter/', views.CommentFilterListApiView.as_view()),
    path('mycomments/', views.CommentAuthorApiView.as_view()),
    path('about/', views.AboutAPI.as_view()),

    # path('login/', views_token.obtain_auth_token),
    path('login/', views.LoginView.as_view()),

    # path('about/', views.AboutTemplateView.as_view()),
]
