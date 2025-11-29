from django.urls import path
from .views import (
    index,
    about,
    InfoRequestCreate,
    register,
    # DESTINATIONS
    destinations,
    show_all_destinations,
    destination_details,
    destination_reviews,
    DestinationUpdateView,
    DestinationDeleteView,
    DestinationReviewCreate,
    purchase_destination,
    # CRUISES
    cruise_details,
    cruise_reviews,
    cruise_review_create,
    CruiseDetailView,
    CruiseReviewCreate,
)
from django.http import HttpResponseNotFound
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.shortcuts import redirect

def favicon_view(request):
    return HttpResponseNotFound("Favicon no encontrado")

def custom_logout_view(request):
    auth_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('index')

urlpatterns = [
    path('', index, name='index'),
    path('info_request/', InfoRequestCreate.as_view(), name='info_request'),
    path('about/', about, name='about'),
    path('favicon.ico', favicon_view),

    # DESTINATIONS
    path('destinations/', destinations, name='destinations'),
    path('destinations/show_all_destinations', show_all_destinations, name='destination_view_all'),
    path('destination/<int:pk>/', destination_details, name='destination_details'),
    path('destination/<int:pk>/reviews/', destination_reviews, name='destination_view_reviews'),
    path('destinations/<int:pk>/reviews/create/', DestinationReviewCreate.as_view(), name='destination_create_reviews'),    path('destination/<int:pk>/edit/', DestinationUpdateView.as_view(), name='destination_confirm_edit'),
    path('destination/<int:pk>/delete/', DestinationDeleteView.as_view(), name='destination_confirm_delete'),
    path('destination/<int:pk>/purchase/', purchase_destination, name='purchase_destination'),
    
    # CRUISES
    path('cruise/<int:pk>/', cruise_details, name='cruise_details'),
    path('cruise/<int:pk>/reviews/', cruise_reviews, name='cruise_view_reviews'),
    path('cruises/<int:pk>/reviews/create/', cruise_review_create, name='cruise_create_reviews'),

    # AUTH
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),

]