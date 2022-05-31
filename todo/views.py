from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .models import ToDo, Comment
from .serializers import NoteSerializer, NoteDetailSerializer, CommentListSerializer
from .filters import *


class NoteListCreateApiView(APIView):
    ordering = ["deadline", "importance"]

    def get(self, request: Request):
        objects = ToDo.objects.all()
        objects = self.order_by_objects(objects)

        serializer = NoteSerializer(instance=objects, many=True)

        return Response(serializer.data)

    def post(self, request: Request):

        serializer = NoteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=request.user)

        return Response(serializer.data)

    def order_by_objects(self, objects):
        return objects.order_by(*self.ordering)



class NoteDetailApiView(APIView):

    def get(self, request: Request, pk):
        note = get_object_or_404(ToDo, pk=pk)
        serializer = NoteDetailSerializer(instance=note)

        return Response(serializer.data)

    def put(self, request: Request, pk):
        note = get_object_or_404(ToDo, pk=pk)
        serializer = NoteDetailSerializer(instance=note, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not note.author == request.user:
            return Response(
                data="Заметка не изменена, ее может изменить только автор",
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(author=request.user)

        return Response(serializer.data)

    def patch(self, request: Request, pk):
        note = get_object_or_404(ToDo, pk=pk)
        serializer = NoteDetailSerializer(instance=note, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not note.author == request.user:
            return Response(
                data="Заметка не изменена, ее может изменить только автор",
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(author=request.user)

        return Response(serializer.data)

    def delete(self, request, pk):
        note = get_object_or_404(ToDo, pk=pk)
        note.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer


class CommentAuthorApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset


class ToDoFilterListApiView(ListAPIView):
    queryset = ToDo.objects.all()
    serializer_class = NoteSerializer

    ordering = ["deadline", "importance"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.order_by_queryset(queryset)

    def filter_queryset(self, queryset):
        queryset = importance_filter(queryset, self.request.query_params.get("importance"))
        queryset = public_filter(queryset, self.request.query_params.get("public"))
        return queryset

    def order_by_queryset(self, queryset):
        return queryset.order_by(*self.ordering)
