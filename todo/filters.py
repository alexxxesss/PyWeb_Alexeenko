from typing import Optional
from django.db.models.query import QuerySet
from django_filters import rest_framework as filters

from .models import ToDo, Comment

def importance_filter(queryset: QuerySet, importance: Optional[bool]):

    if importance is not None:
        return queryset.filter(importance=importance)
    else:
        return queryset


def public_filter(queryset: QuerySet, public: Optional[bool]):

    if public is not None:
        return queryset.filter(public=public)
    else:
        return queryset


def filter_by_author_id(queryset: QuerySet, author_id: Optional[int]):
    if author_id is not None:
        return queryset.filter(author=author_id)
    else:
        return queryset


class ToDoFilter(filters.FilterSet):
    ...

    class Meta:
        model = ToDo
        fields = [
            'importance',
            'public',
            'author',
            'status',
        ]
