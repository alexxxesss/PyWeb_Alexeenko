from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def datetime_now_plus_one_day():
    return datetime.now() + timedelta(days=1)


class ToDo(models.Model):
    """Заметки"""

    class StatusChoices(models.TextChoices):
        ACTIVE = 'Active', _('Активно')
        DELAYED = 'Delayed', _('Отложено')
        FINISH = 'Finish', _('Выполнено')

    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    message = models.TextField(verbose_name=_("Текст заметки"))
    public = models.BooleanField(default=False, verbose_name=_("Публичная"))
    importance = models.BooleanField(default=False, verbose_name=_("Важно"))
    status = models.CharField(max_length=15, default=StatusChoices.DELAYED,
                              choices=StatusChoices.choices, verbose_name=_("Статус"))
    deadline = models.DateTimeField(default=datetime_now_plus_one_day,
                                    verbose_name=_("Крайний срок"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Время создания"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Время обновления"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Автор"))

    def __str__(self):
        return f"Запись №{self.id}"

    class Meta:
        verbose_name = _("запись")
        verbose_name_plural = _("записи")


class Comment(models.Model):
    """Комментарии с оценками к заметкам"""
    class Rating(models.IntegerChoices):
        WITHOUT_RATING = 0, _('Без оценки')
        TERRIBLE = 1, _('Ужасно')
        BADLY = 2, _('Плохо')
        FINE = 3, _('Нормально')
        GOOD = 4, _('Хорошо')
        EXCELLENT = 5, _('Отлично')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Автор"))
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE, related_name="comments", verbose_name=_("Запись"))
    text_comment = models.TextField(verbose_name=_("Текст комментария"))
    rating = models.IntegerField(default=Rating.WITHOUT_RATING, choices=Rating.choices, verbose_name=_("Оценка"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Время создания комментария"))

    class Meta:
        verbose_name = _("комментарий")
        verbose_name_plural = _("комментарии")

    def __str__(self):
        return f'{self.get_rating_display()}: {self.author}'
