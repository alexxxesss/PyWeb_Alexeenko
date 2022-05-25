from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    # Поля в списке
    list_display = ('title', 'public', 'id', 'update_at', 'author')
    ##
    #  Группировка полей в режиме редактирования
    fields = (('title', 'public'), 'message', 'update_at', 'create_at', 'author')
    ##
    #  Поля только для чтения в режиме редактирования
    readonly_fields = ('update_at', 'create_at')
    ##
    #  Поиск по выбранным полям
    search_fields = ['title', 'message', 'author']
    ##
    #  Фильтры справа
    list_filter = ('public',)
