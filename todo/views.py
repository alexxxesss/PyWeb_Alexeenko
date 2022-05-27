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

    def get(self, request: Request):

        objects = ToDo.objects.all()
        serializer = NoteSerializer(instance=objects, many=True)

        return Response(serializer.data)

    def post(self, request: Request):

        serializer = NoteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=request.user)

        return Response(serializer.data)


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
                status=status.HTTP_400_BAD_REQUEST
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
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(author=request.user)

        return Response(serializer.data)

    def delete(self, request, pk):
        note = get_object_or_404(ToDo, pk=pk)
        del_note = note.delete()

        return Response(del_note)


class CommentListApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer


class ToDoFilterListApiView(ListAPIView):
    queryset = ToDo.objects.all()
    serializer_class = NoteSerializer

    def filter_queryset(self, queryset):
        queryset = importance_filter(queryset, self.request.query_params.get("importance"))
        queryset = public_filter(queryset, self.request.query_params.get("public"))
        return queryset
