from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from users.models import Schedule, Sportsman, TrainingResponse


@login_required
def respond_to_training(request, schedule_id, action):
    sportsman = get_object_or_404(Sportsman, user=request.user)
    schedule = get_object_or_404(Schedule, id=schedule_id)

    response, created = TrainingResponse.objects.get_or_create(
        schedule=schedule,
        sportsman=sportsman
    )

    if action == 'accept':
        response.status = 'accepted'
    elif action == 'decline':
        response.status = 'declined'
    
    response.save()
    return redirect('users:schedule_detail', pk=schedule_id)
