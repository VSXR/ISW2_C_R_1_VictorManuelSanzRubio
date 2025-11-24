## APP (relecloud)
# MIRAR VIEWS.PY --> CONTIENEN LAS FUNCIONES QUE RENDERIZAN LAS PAGINAS

from django.urls import path
from . import views
from django.http import HttpResponseNotFound

def favicon_view(request):
    return HttpResponseNotFound("Favicon no encontrado")

# URLS
urlpatterns = [
    # route, view where we will display our data, name of the view
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),
    path('destination/<int:pk>', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('destination/add', views.DestinationDetailView.as_view(), name='destination_form'),

    path('destination/<int:pk>/update', views.DestinationUpdateView.as_view(), name='destination_form'),
    path('destination/<int:pk>/delete', views.DestinationDeleteView.as_view(), name='destination_confirm_delete'),

    path('cruise/<int:pk>', views.CruiseDetailView.as_view(), name='cruise_detail'),
    path('info_request/', views.InfoRequestCreate.as_view(), name='info_request'),
    
    # Otras rutas
    path('favicon.ico', favicon_view),
]
