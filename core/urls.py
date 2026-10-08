from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("listings/", views.listings, name="listings"),
    path("listing/<int:pk>/", views.listing_detail, name="listing_detail"),
    path("listing/<int:pk>/request/", views.request_item, name="request_item"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("donate/", views.create_listing, name="create_listing"),
    path("request/<int:pk>/<str:action>/", views.update_request, name="update_request"),
    path("map/", views.map_view, name="map"),
    path("volunteer-map/", views.volunteer_map, name="volunteer_map"),
    path("api/volunteer/location/", views.update_volunteer_location, name="update_volunteer_location"),
    path("api/volunteer/location/current/", views.get_volunteer_location, name="get_volunteer_location"),
]
