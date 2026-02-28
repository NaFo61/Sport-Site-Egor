from django.contrib import admin

from training.models import (
    Training,
    Exercise,
    ProgressLog,
)

class ExerciseInline(admin.TabularInline):
    """Позволяет добавлять упражнения прямо внутри тренировки"""
    model = Exercise
    extra = 1
    fields = ('order', 'name', 'sets', 'repetitions', 'rest_seconds')
    ordering = ('order',)

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'training_type',
        'group',
        'coach',
        'date',
        'duration_minutes',
    )
    list_filter = ('training_type', 'group', 'coach', 'date')
    search_fields = ('title', 'coach__username', 'coach__first_name', 'coach__last_name')
    list_select_related = ('training_type', 'group', 'coach')
    inlines = [ExerciseInline]
    ordering = ('-date',)
    date_hierarchy = 'date'

@admin.register(ProgressLog)
class ProgressLogAdmin(admin.ModelAdmin):
    list_display = (
        'athlete',
        'exercise',
        'date',
        'completed_sets',
        'actual_repetitions',
        'weight_kg',
    )
    list_filter = ('date', 'exercise')
    search_fields = (
        'athlete__username',
        'athlete__first_name',
        'athlete__last_name',
        'exercise__name',
        'exercise__training__title',
    )
    list_select_related = ('athlete', 'exercise', 'exercise__training')
    ordering = ('-date',)
