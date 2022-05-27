from django.urls import path

from . import views

urlpatterns = [
    path('todo/', views.NoteListCreateApiView.as_view()),
    path('todo/<int:pk>/', views.NoteDetailApiView.as_view()),
    path('comments/', views.CommentListApiView.as_view()),
    path('todo/filters/', views.ToDoFilterListApiView.as_view()),
]
