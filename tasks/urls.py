from tasks.views import events_dashboard, managerdashboard, user_dashboard, dashboard, create_events, view_events, create_participent, delete_event, update_event, navbar
from django.urls import path

urlpatterns = [
    
    path("events-dashboard/", events_dashboard, name='events-dashboard'),
    path("manager-dashboard/", managerdashboard, name='manager-dashboard'),
    path("user-dashboard/", user_dashboard, name="user-dashboard"),
    path("dashboard/", dashboard),
    path("create-events/", create_events, name="create-events"),
    path("update-events/<int:id>/", update_event, name="update-events"),
    path("delete-events/<int:id>/", delete_event, name="delete-events"),
    path("create-participent/", create_participent, name="create-participent"),
    path("view-participent/", view_events, name="view-participent"),
    path("navbar/", navbar, name="navbar")
]
