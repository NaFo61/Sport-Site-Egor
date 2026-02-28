from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),
    
    path('calendar/', views.calendar_view, name='calendar'),
    path("calendar/day/<str:day>/", views.calendar_day_view, name="calendar_day"),
    
    path('create-invitation/', views.create_invitation, name='create_invitation'),
    path('my-invitations/', views.my_invitations, name='my_invitations'),
    
    path('response/<int:response_id>/accept/', views.accept_schedule, name='accept_schedule'),
    path('response/<int:response_id>/decline/', views.decline_schedule, name='decline_schedule'),

    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/<int:notif_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_read, name='mark_all_read'),
]
