from tasks.views import search_event, organizer_dashboard, view_participents, participent_dashboard, dashboard, create_events, delete_event, update_event, event_details, dashboard, CreateEvents
from django.urls import path
from core.views import home

urlpatterns = [
    
    # path("", home, name="home"),
    # path("events-dashboard/", search_event, name='events-dashboard'),
    path("searched-result/", search_event, name='searched-result'),
    path("organizer-dashboard/", organizer_dashboard, name='organizer-dashboard'),
    path("dashboard/", dashboard, name='dashboard'),
    # path("create-events/", create_events, name="create-events"),
    path("create-events/", CreateEvents.as_view(), name="create-events"),
    path("update-events/<int:id>/", update_event, name="update-events"),
    path("delete-events/<int:id>/", delete_event, name="delete-events"),
    # path("create-participent/", create_participent, name="create-participent"),
    path("view-participent/", view_participents, name="view-participent"),
    path("events/<int:event_id>/details", event_details, name="event-details"),
    
    
    
]
