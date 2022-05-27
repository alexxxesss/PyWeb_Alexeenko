from typing import Optional
from django.db.models.query import QuerySet


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


def active_status_filter(self, queryset: QuerySet):
    ...


def delayed_status_filter(self, queryset: QuerySet):
    ...


def finish_status_filter(self, queryset: QuerySet):
    ...
