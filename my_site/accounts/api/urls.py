from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.user_create_api_view, name="user-create-api"),
    
]