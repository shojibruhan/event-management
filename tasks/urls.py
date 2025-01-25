from tasks.views import show_task
from django.urls import path

urlpatterns = [
    path("show-task/", show_task)
]
