from django.urls import path
from users.views import sign_in, sign_up, sign_out, activate_user, admin_dashboard, assign_role, create_group, group_list, events_list, rspv_event, my_events, participant_dashboard

urlpatterns = [
    path("sign-up/", sign_up, name='sign-up'),
    path("sign-in/", sign_in, name='sign-in'),
    path("sign-out/", sign_out, name='sign-out'),
    path("activate/<int:user_id>/<str:token>/", activate_user),
    path("admin/dashboard/", admin_dashboard, name="admin-dashboard"),
    path("admin/<int:user_id>/assign-role/", assign_role, name= "assign-role"),
    path("admin/create-group", create_group, name="create-group"),
    path("admin/group-list/", group_list, name="group-list" ),
    path("admin/events-list/", events_list, name='events-list'),
    path('rsvm/<int:event_id>/', rspv_event, name='rsvm'),
    path('my-events/', my_events, name='my-events'),
    path("participant-dashboard/", participant_dashboard, name="participant-dashboard"),
     
]
