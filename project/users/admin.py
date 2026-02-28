from django.contrib import admin

from users.models import (
    Trainer,
    TrainingType,
    TrainingGroup,
    Sportsman,
    Schedule,
    TrainingResponse,
    TrainerTrainingType,
    Notification,
)


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_avatar_url')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(TrainingType)
class TrainingTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(TrainingGroup)
class TrainingGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    search_fields = ("title",)
    list_filter = ("is_active",)
    ordering = ("title",)


@admin.register(Sportsman)
class SportsmanAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "main_trainer",
        "training_group",
        "is_active",
    )
    list_filter = ("is_active", "training_group", "main_trainer")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    ordering = ("user",)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("training_type", "start_time", "finish_time", "status", "type")
    list_filter = ("status", "type", "training_type")
    ordering = ("-start_time",)
    date_hierarchy = "start_time"
    search_fields = ("training_type__name", "group__title", "sportsman__user__username")


@admin.register(TrainingResponse)
class TrainingResponseAdmin(admin.ModelAdmin):
    list_display = ("schedule", "sportsman", "status")
    list_filter = ("status",)
    search_fields = ("sportsman__user__username", "schedule__training_type__name")
    ordering = ("schedule",)


@admin.register(TrainerTrainingType)
class TrainerTrainingTypeAdmin(admin.ModelAdmin):
    list_display = ("trainer", "training_type")
    search_fields = ("trainer__user__username", "training_type__name")
    ordering = ("trainer",)



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("user__username", "message")
    ordering = ("-created_at",)
