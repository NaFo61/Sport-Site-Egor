from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Training(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    training_type = models.ForeignKey(
        'users.TrainingType',
        on_delete=models.PROTECT,
        related_name='trainings',
        verbose_name='Тип тренировки'
    )

    group = models.ForeignKey(
        'users.TrainingGroup',
        on_delete=models.CASCADE,
        related_name='trainings',
        null=True,
        blank=True,
        verbose_name='Группа'
    )

    coach = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_trainings',
        verbose_name='Тренер'
    )

    date = models.DateTimeField(default=timezone.now, verbose_name='Дата проведения')
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, verbose_name='Длительность (мин.)')
    notes = models.TextField(blank=True, verbose_name='Заметки и комментарии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        ordering = ['-date']
        verbose_name = "тренировка"
        verbose_name_plural = "тренировки"

    def __str__(self):
        return f"{self.title} — {self.date:%d.%m.%Y}"


class Exercise(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='exercises', verbose_name='Тренировка')
    name = models.CharField(max_length=200, verbose_name='Название упражнения')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок выполнения')
    sets = models.PositiveIntegerField(default=1, verbose_name='Подходы')
    repetitions = models.CharField(max_length=100, blank=True, verbose_name='Повторения/время')
    rest_seconds = models.PositiveIntegerField(null=True, blank=True, verbose_name='Отдых (сек)')

    class Meta:
        ordering = ['order']
        verbose_name = "упражнение"
        verbose_name_plural = "упражнения"

    def __str__(self):
        return f"{self.name} (#{self.order})"


class ProgressLog(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='logs', verbose_name='Упражнение')
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_logs', verbose_name='Спортсмен')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    notes = models.TextField(blank=True, verbose_name='Комментарий')
    completed_sets = models.PositiveIntegerField(null=True, blank=True, verbose_name='Выполнено подходов')
    actual_repetitions = models.CharField(max_length=100, blank=True, verbose_name='Факт. повторения')
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Вес (кг)')

    class Meta:
        ordering = ['-date']
        verbose_name = "лог прогресса"
        verbose_name_plural = "логи прогресса"

    def __str__(self):
        return f"{self.athlete} — {self.exercise.name} ({self.date:%d.%m.%Y})"
