from tasks.views import home, search_event, managerdashboard, view_events, user_dashboard, dashboard, create_events, delete_event, update_event, navbar
from django.urls import path

urlpatterns = [
    
    path("", home, name="home"),
    # path("events-dashboard/", search_event, name='events-dashboard'),
    path("searched-result/", search_event, name='searched-result'),
    path("manager-dashboard/", managerdashboard, name='manager-dashboard'),
    path("user-dashboard/", user_dashboard, name="user-dashboard"),
    path("dashboard/", dashboard),
    path("create-events/", create_events, name="create-events"),
    path("update-events/<int:id>/", update_event, name="update-events"),
    path("delete-events/<int:id>/", delete_event, name="delete-events"),
    # path("create-participent/", create_participent, name="create-participent"),
    path("view-participent/", view_events, name="view-participent"),
    path("navbar/", navbar, name="navbar"),
    
]
