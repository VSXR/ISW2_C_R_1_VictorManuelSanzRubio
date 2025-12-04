from .destination import (
    destinations,
    show_all_destinations,
    destination_details,
    DestinationUpdateView,
    DestinationDeleteView,
    DestinationReviewCreate,
    purchase_destination,
)
from .cruise import (
    cruise_details,
    cruise_reviews,
    cruise_review_create,
    purchase_cruise,
    CruiseDetailView,
    CruiseReviewCreate,
)
from .review import (
    destination_reviews,
    destination_review_create,
    cruise_reviews,
    # cruise_review_create,
)
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from ..models import InfoRequest
from ..forms import InfoRequestForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from typing import cast
from django.forms import ModelForm

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = InfoRequest
    form_class = InfoRequestForm
    success_message = "Thank you, %(name)s! Your request has been sent successfully. Check your email for more information about our cruises!"

    def form_valid(self, form):
        form = cast(ModelForm, form)
        response = super().form_valid(form)
        info_request = form.instance
        subject = 'Info Request Received'
        message = render_to_string('info_request_email.txt', {
            'name': info_request.name,
            'cruise_name': info_request.cruise.name,
        })
        send_mail(
            subject,
            message,
            'c4relecloud@gmail.com',
            [info_request.email],
            fail_silently=False,
        )
        return response