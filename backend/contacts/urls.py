from django.urls import path

from . import views

urlpatterns = [
    path("messages/", views.create_message, name="create-message"),
]
