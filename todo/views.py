from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import ToDo, Comment
from .serializers import *
from .filters import *
from .settings_local import SERVER_VERSION


class NoteListCreateApiView(APIView):
    permission_classes = (IsAuthenticated, )
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

        if not note.author == request.user:
            return Response(
                data="Заметка не удалена, ее может удалить только автор",
                status=status.HTTP_403_FORBIDDEN
            )

        note.delete()

        return Response(data="Запись удалена", status=status.HTTP_204_NO_CONTENT)


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

    filter_backends = [DjangoFilterBackend]
    filterset_class = ToDoFilter

    ordering = ["deadline", "importance"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.order_by_queryset(queryset)

    def order_by_queryset(self, queryset):
        return queryset.order_by(*self.ordering)


class AboutAPI(View):
    def get(self, request):
        template = "todo/about.html"
        context = {
            "server_version": SERVER_VERSION,
            "user_name": request.user
        }
        return render(request, template_name=template, context=context)


# class AboutTemplateView(TemplateView):
#     """
#     Второй способ сформировать страничку About
#     """
#     template_name = "todo/about.html"
#
#     def get(self, request,  *args, **kwargs):
#         context = super().get_context_data()
#         context["user_name"] = request.user
#         context["server_version"] = SERVER_VERSION
#         return self.render_to_response(context)


class CommentFilterListApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer

    def filter_queryset(self, queryset):
        query_params = QueryParamsCommentFilterSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)

        list_rating = query_params.data.get("rating")
        author = self.request.query_params.get("author")

        if list_rating:
            queryset = queryset.filter(rating__in=query_params.data["rating"])

        if author:
            queryset = queryset.filter(author__username=author)

        return queryset


class LoginView(APIView):
    def post(self, request: Request):
        user = authenticate(
            username=request.data['username'],
            password=request.data['password']
        )
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
