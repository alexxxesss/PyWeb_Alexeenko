from django.urls import path

from . import views

urlpatterns = [
    path('notes/', views.NoteListCreateApiView.as_view()),
    path('notes/<int:pk>/', views.NoteDetailApiView.as_view()),
]
