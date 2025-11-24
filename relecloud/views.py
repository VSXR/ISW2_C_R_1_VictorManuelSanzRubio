# MIRAR URLS.PY --> CONTIENEN LAS RUTAS DE LA APLICACION

from django.shortcuts import render, HttpResponse
from . import models
from django import forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
def index(request):
    return render(request, 'index.html')

def requestInformation(request):
    return render(request, 'info_request_create.html')

def destinations(request):
    all_destinations = models.Destination.objects.all()
    return render(request, 'destinations.html', {'destinations': all_destinations})

def about(request):
    return render(request, 'about.html')

class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

class DestinationUpdateView(generic.UpdateView):
    template_name = 'destination_form.html'
    model = models.Destination
    fields = ['name', 'desc']

class DestinationDeleteView(generic.DeleteView):
    template_name = 'destination_confirm_delete.html'
    model = models.Destination
    success_url = reverse_lazy('destinations')

class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'


# Formulario para InfoRequest que incluye el campo de selección de crucero
class InfoRequestForm(forms.ModelForm):
    class Meta:
        model = models.InfoRequest
        fields = ['name', 'email', 'phone', 'message', 'cruise']  # Incluye el campo 'cruise'

# Vista para manejar la creación de InfoRequest
class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    form_class = InfoRequestForm
    success_url = reverse_lazy('index')
    success_message = "Thank you, %(name)s! Your request has been sent successfully. Check your email for more information about our cruises!"