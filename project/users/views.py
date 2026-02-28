import calendar

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Q
from datetime import date, datetime, timedelta, time
from django.utils.timezone import now, make_aware

from django.http import Http404
from .models import Schedule, TrainingResponse, Notification, Sportsman, Trainer
from .forms import InviteSportsmenForm




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Аккаунт {username} создан! Добро пожаловать!')
            return redirect('users:profile')
    else:
        form = UserCreationForm()
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    sportsman = None
    trainer = None
    user_type = None
    responses = None

    try:
        sportsman = request.user.sportsman
        user_type = 'sportsman'
        responses = TrainingResponse.objects.filter(
            sportsman=sportsman, status='waiting'
        ).select_related('schedule__training_type').order_by('-schedule__start_time')
        upcoming_trainings = Schedule.objects.filter(
            start_time__gte=timezone.now(),
            status='scheduled'
        ).filter(
            Q(group=sportsman.training_group, type='group') |
            Q(sportsman=sportsman, type='individual')
        ).select_related('training_type', 'trainer', 'group').order_by('start_time')[:5]
    
    except Sportsman.DoesNotExist:
        pass

    try:
        trainer = request.user.trainer
        user_type = 'trainer'
        upcoming_trainings = Schedule.objects.filter(
            trainer=trainer,
            start_time__gte=timezone.now(),
            status='scheduled'
        ).select_related(
            'training_type', 'sportsman', 'group'
        ).order_by('start_time')[:5]
    except Trainer.DoesNotExist:
        pass

    context = {
        'user_type': user_type,
        'sportsman': sportsman,
        'trainer': trainer,
        'responses': responses,
        'upcoming_trainings': upcoming_trainings if 'upcoming_trainings' in locals() else [],
    }
    return render(request, 'users/profile.html', context)


def is_trainer(user):
    return hasattr(user, 'trainer')


def build_month(year, month, trainings_qs):
    cal = calendar.Calendar(firstweekday=0)
    weeks = []

    for week in cal.monthdatescalendar(year, month):
        week_days = []
        for day in week:
            if day.month != month:
                week_days.append(None)
            else:
                day_trainings = [
                    t for t in trainings_qs
                    if t.start_time.date() == day
                ]
                week_days.append({
                    "date": day,
                    "trainings": day_trainings
                })
        weeks.append(week_days)

    month_title = date(year, month, 1).strftime('%B %Y').capitalize()

    return {
        "title": month_title,
        "weeks": weeks,
        "trainings": trainings_qs,
    }


def month_range(year, month):
    start = date(year, month, 1)

    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)

    return start, end


@login_required
def calendar_view(request):
    user = request.user
    today = now()

    base_qs = Schedule.objects.none()

    if hasattr(user, 'trainer'):
        base_qs = Schedule.objects.filter(
            trainer=user.trainer,
            start_time__gte=today
        )

    elif hasattr(user, 'sportsman'):
        sportsman = user.sportsman
        base_qs = Schedule.objects.filter(
            start_time__gte=today
        ).filter(
            Q(group=sportsman.training_group, type='group') |
            Q(sportsman=sportsman, type='individual')
        )
        individual_ids = []
        for schedule in base_qs.filter(type='individual'):
            if schedule.is_accepted_by_sportsman(sportsman):
                individual_ids.append(schedule.id)
        
        base_qs = base_qs.filter(
            Q(type='group') | Q(id__in=individual_ids)
        )

    base_qs = base_qs.select_related(
        'training_type', 'trainer', 'sportsman', 'group'
    )

    current_year = today.year
    current_month = today.month

    cur_start, cur_end = month_range(current_year, current_month)

    trainings_current = base_qs.filter(
        start_time__date__gte=cur_start,
        start_time__date__lt=cur_end
    ).order_by('start_time')

    next_month_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1)

    next_start, next_end = month_range(
        next_month_date.year,
        next_month_date.month
    )

    trainings_next = base_qs.filter(
        start_time__date__gte=next_start,
        start_time__date__lt=next_end
    ).order_by('start_time')

    months = [
        build_month(current_year, current_month, trainings_current),
        build_month(next_month_date.year, next_month_date.month, trainings_next),
    ]

    return render(request, 'users/calendar.html', {
        'months': months,
        'today': timezone.now()
    })


@login_required
def calendar_day_view(request, day):
    try:
        selected_date = datetime.strptime(day, "%Y-%m-%d").date()
    except ValueError:
        raise Http404("Неверная дата")

    user = request.user

    day_start = make_aware(datetime.combine(selected_date, time.min))
    day_end = make_aware(datetime.combine(selected_date, time.max))

    trainings = Schedule.objects.none()

    if hasattr(user, "trainer"):
        trainings = Schedule.objects.filter(
            trainer=user.trainer,
            start_time__range=(day_start, day_end)
        )

    elif hasattr(user, "sportsman"):
        sportsman = user.sportsman
        trainings = Schedule.objects.filter(
            start_time__range=(day_start, day_end)
        ).filter(
            Q(group=sportsman.training_group, type='group') |
            Q(sportsman=sportsman, type='individual')
        )
        
        individual_ids = []
        for schedule in trainings.filter(type='individual'):
            if schedule.is_accepted_by_sportsman(sportsman):
                individual_ids.append(schedule.id)
        
        trainings = trainings.filter(
            Q(type='group') | Q(id__in=individual_ids)
        )

    trainings = trainings.select_related(
        "training_type", "trainer", "sportsman", "group"
    ).order_by("start_time")

    return render(request, "users/calendar_day.html", {
        "selected_date": selected_date,
        "trainings": trainings,
    })


@login_required
@user_passes_test(is_trainer, login_url='users:profile')
def create_invitation(request):
    trainer = request.user.trainer
    
    if request.method == 'POST':
        form = InviteSportsmenForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.status = 'scheduled'
            
            sportsmen = form.cleaned_data['sportsmen']
            if sportsmen.count() > 1:
                schedule.type = 'group'
                schedule.group = sportsmen.first().training_group
                schedule.trainer = trainer
            else:
                schedule.type = 'individual'
                schedule.sportsman = sportsmen.first()
                schedule.trainer = trainer

            schedule.save()

            for sportsman in sportsmen:
                response, created = TrainingResponse.objects.get_or_create(
                    schedule=schedule,
                    sportsman=sportsman,
                    defaults={'status': 'waiting'}
                )

                if created:
                    message = (
                        f'Вы приглашены на тренировку "{schedule.training_type.name}" '
                        f'{schedule.start_time.strftime("%d.%m.%Y в %H:%M")}. '
                        f'Тренер: {trainer.user.get_full_name() or trainer.user.username}'
                    )
                else:
                    message = (
                        f'Напоминание о тренировке "{schedule.training_type.name}" '
                        f'{schedule.start_time.strftime("%d.%m.%Y в %H:%M")}'
                    )

                Notification.objects.create(
                    user=sportsman.user,
                    message=message
                )
            
            messages.success(
                request,
                f'Приглашение отправлено {sportsmen.count()} спортсмену(ам)'
            )
            return redirect('users:calendar')
    else:
        form = InviteSportsmenForm()
    
    return render(request, 'users/create_invitation.html', {
        'form': form,
        'trainer': trainer
    })


@login_required
def my_invitations(request):
    if not hasattr(request.user, 'sportsman'):
        messages.error(request, 'Только спортсмены могут видеть приглашения')
        return redirect('users:profile')
    
    sportsman = request.user.sportsman

    responses = TrainingResponse.objects.filter(
        sportsman=sportsman
    ).select_related('schedule__training_type').order_by('-schedule__start_time')
    
    return render(request, 'users/my_invitations.html', {
        'responses': responses,
        'sportsman': sportsman
    })


@login_required
@require_POST
def accept_schedule(request, response_id):
    user = request.user
    
    if not hasattr(user, 'sportsman'):
        messages.error(request, 'Только спортсмены могут принимать приглашения')
        return redirect('users:my_invitations')
    
    with transaction.atomic():
        resp = get_object_or_404(TrainingResponse, id=response_id)
        
        if resp.sportsman.user != user:
            messages.error(request, 'Нет прав для изменения этого ответа')
            return redirect('users:my_invitations')
        
        resp.status = 'accepted'
        resp.save()

        Notification.objects.filter(
            user=user,
            message__contains=resp.schedule.training_type.name
        ).update(is_read=True)
        
        messages.success(request, 'Приглашение принято!')
    
    return redirect('users:my_invitations')


@login_required
@require_POST
def decline_schedule(request, response_id):
    user = request.user
    
    if not hasattr(user, 'sportsman'):
        messages.error(request, 'Только спортсмены могут отклонять приглашения')
        return redirect('users:my_invitations')
    
    with transaction.atomic():
        resp = get_object_or_404(TrainingResponse, id=response_id)
        
        if resp.sportsman.user != user:
            messages.error(request, 'Нет прав для изменения этого ответа')
            return redirect('users:my_invitations')
        
        resp.status = 'declined'
        resp.save()
        
        Notification.objects.filter(
            user=user,
            message__contains=resp.schedule.training_type.name
        ).update(is_read=True)
        
        messages.success(request, 'Приглашение отклонено')
    
    return redirect('users:my_invitations')


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    return render(request, 'users/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
@require_POST
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('users:notifications')


@login_required
@require_POST
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'Все уведомления отмечены как прочитанные')
    return redirect('users:notifications')


def home(request):
    context = {'user': request.user}
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'sportsman'):
            sportsman = request.user.sportsman
            upcoming = Schedule.objects.filter(
                start_time__gte=timezone.now(),
                status='scheduled'
            ).filter(
                Q(group=sportsman.training_group, type='group') |
                Q(sportsman=sportsman, type='individual')
            )
            individual_ids = []
            for schedule in upcoming.filter(type='individual'):
                if schedule.is_accepted_by_sportsman(sportsman):
                    individual_ids.append(schedule.id)
            
            upcoming = upcoming.filter(
                Q(type='group') | Q(id__in=individual_ids)
            ).order_by('start_time')[:5]
            
            context.update({
                'upcoming_trainings': upcoming,
                'unread_notifications': request.user.notifications.filter(is_read=False).count(),
            })

        elif hasattr(request.user, 'trainer'):
            upcoming = Schedule.objects.filter(
                Q(trainer=request.user.trainer),
                start_time__gte=timezone.now(),
                status='scheduled'
            ).order_by('start_time')[:5]
            context.update({
                'upcoming_trainings': upcoming,
                'unread_notifications': request.user.notifications.filter(is_read=False).count(),
            })
    
    return render(request, 'users/home.html', context)
