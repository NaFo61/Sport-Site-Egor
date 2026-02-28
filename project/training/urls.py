from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('respond/<int:schedule_id>/<str:action>/', views.respond_to_training, name='respond_to_training'),
]
