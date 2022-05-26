from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .models import Note, Comment
from .serializers import NoteSerializer, NoteDetailSerializer, CommentSerializer


class NoteListCreateApiView(APIView):

    def get(self, request: Request):

        objects = Note.objects.all()
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
        note = get_object_or_404(Note, pk=pk)
        serializer = NoteDetailSerializer(instance=note)

        return Response(serializer.data)

    def post(self, request: Request):
        ...
