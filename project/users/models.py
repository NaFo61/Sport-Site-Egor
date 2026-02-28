from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def user_avatar_path(instance, filename):
    user_id = instance.user.id if instance.user and instance.user.id else 'unknown'
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    return f'avatars/user_{user_id}/{timestamp}_{filename}'


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True, verbose_name="Аватар")

    def __str__(self):
        return f"Тренер {self.user.get_full_name() if self.user else 'Без пользователя'}"

    def get_avatar_url(self):
        return self.avatar.url if self.avatar else "/static/images/default_avatar.png"

    class Meta:
        verbose_name = "тренер"
        verbose_name_plural = "тренеры"


class TrainingType(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')

    class Meta:
        verbose_name = 'тип тренировки'
        verbose_name_plural = 'типы тренировок'

    def __str__(self):
        return self.name


class TrainingGroup(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Активная группа')

    class Meta:
        verbose_name = 'тренировочная группа'
        verbose_name_plural = 'тренировочные группы'

    def __str__(self):
        return self.title


class Sportsman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True, verbose_name="Аватар")
    birth_date = models.DateField(verbose_name='Дата рождения')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    main_trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Основной тренер', related_name='sportsmen')
    razryad = models.CharField(max_length=128, verbose_name='Разряд', blank=True, null=True)
    training_group = models.ForeignKey('TrainingGroup', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тренировочная группа')

    class Meta:
        verbose_name = 'спортсмен'
        verbose_name_plural = 'спортсмены'

    def __str__(self):
        return f"Спортсмен {self.user.get_full_name() if self.user else '— Без пользователя —'}"

    def get_avatar_url(self):
        return self.avatar.url if self.avatar else "/static/images/default_avatar.png"


class Schedule(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Запланирована'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    TYPE_CHOICES = [
        ('individual', 'Индивидуальная'),
        ('group', 'Групповая'),
    ]

    training_type = models.ForeignKey('TrainingType', on_delete=models.CASCADE, verbose_name='Тип тренировки')
    start_time = models.DateTimeField(verbose_name='Время начала')
    finish_time = models.DateTimeField(verbose_name='Время окончания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name='Статус')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип занятия')
    sportsman = models.ForeignKey('Sportsman', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Спортсмен')
    group = models.ForeignKey('TrainingGroup', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Группа')
    description = models.TextField(blank=True, verbose_name='Описание')  # ← ДОБАВЛЕНО
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, verbose_name="Тренер")

    class Meta:
        verbose_name = 'расписание'
        verbose_name_plural = 'расписания'

    def __str__(self):
        return f"{self.training_type} — {self.start_time:%d.%m.%Y %H:%M}"

    def is_accepted_by_sportsman(self, sportsman):
        if self.type == 'group':
            return True
        elif self.type == 'individual' and self.sportsman == sportsman:
            response = self.responses.filter(sportsman=sportsman).first()
            return response and response.status == 'accepted'
        return False

    def is_declined_by_sportsman(self, sportsman):
        if self.type == 'group':
            return False
        elif self.type == 'individual' and self.sportsman == sportsman:
            response = self.responses.filter(sportsman=sportsman).first()
            return response and response.status == 'declined'
        return False

    def is_visible_for_sportsman(self, sportsman):
        if self.type == 'group':
            return self.group == sportsman.training_group
        elif self.type == 'individual':
            return (self.sportsman == sportsman and 
                    self.is_accepted_by_sportsman(sportsman))
        return False

class TrainingResponse(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Ожидает ответа'),
        ('accepted', 'Принял'),
        ('declined', 'Отклонил'),
    ]
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='responses', verbose_name='Тренировка')
    sportsman = models.ForeignKey('Sportsman', on_delete=models.CASCADE, related_name='responses', verbose_name='Спортсмен')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name='Статус')

    class Meta:
        verbose_name = 'ответ спортсмена'
        verbose_name_plural = 'ответы спортсменов'
        unique_together = ('schedule', 'sportsman')

    def __str__(self):
        return f"{self.sportsman} → {self.schedule} ({self.get_status_display()})"


class TrainerTrainingType(models.Model):
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, verbose_name='Тренер')
    training_type = models.ForeignKey('TrainingType', on_delete=models.CASCADE, verbose_name='Тип тренировки')

    class Meta:
        verbose_name = 'тип тренировки тренера'
        verbose_name_plural = 'типы тренировок тренеров'
        unique_together = ['trainer', 'training_type']

    def __str__(self):
        return f"{self.trainer} - {self.training_type}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255, verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'

    def __str__(self):
        return f"Уведомление для {self.user.username}: {self.message[:40]}"
