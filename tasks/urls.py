from tasks.views import show_task, events_dashboard, managerdashboard, user_dashboard, dashboard, create_task
from django.urls import path

urlpatterns = [
    path("show-task/", show_task),
    path("events-dashboard/", events_dashboard, name='events-dashboard'),
    path("manager-dashboard/", managerdashboard, name='manager-dashboard'),
    path("user-dashboard/", user_dashboard, name="user-dashboard"),
    path("dashboard/", dashboard),
    path("create-task/", create_task)
]
