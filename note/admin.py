from django.contrib import admin

from .models import Note, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Поля в списке
    list_display = ('author', 'note', 'text_comment', 'rating', 'created')
    ##
    #  Группировка полей в режиме редактирования
    fields = (('author', 'note'), 'text_comment', 'rating', 'created')
    ##
    #  Поля только для чтения в режиме редактирования
    readonly_fields = ('created',)
    ##
    #  Поиск по выбранным полям
    search_fields = ['text_comment']
    ##
    #  Фильтры справа
    list_filter = ('author', 'rating')


class CommentInline(admin.TabularInline):
    model = Comment

    extra = 0
    min_num = 0


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # Поля в списке
    list_display = ('title', 'public', 'importance', 'status', 'deadline', 'update_at', 'author')
    ##
    #  Группировка полей в режиме редактирования
    fields = (('title', 'public', 'importance'), 'deadline', 'author', 'status', 'message', 'update_at', 'create_at')
    ##
    #  Поля только для чтения в режиме редактирования
    readonly_fields = ('update_at', 'create_at')
    ##
    #  Поиск по выбранным полям
    search_fields = ['title', 'message', 'author']
    ##
    #  Фильтры справа
    list_filter = ('public', 'importance', 'status')

    inlines = [CommentInline]
