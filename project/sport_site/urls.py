from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('training/', include('training.urls', namespace='training')),
    path('', user_views.home, name='home'),  # главная страница
]
