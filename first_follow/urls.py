from django.urls import path
from first_follow import views

urlpatterns = [
    path('', views.first_follow, name='first_follow'),
]