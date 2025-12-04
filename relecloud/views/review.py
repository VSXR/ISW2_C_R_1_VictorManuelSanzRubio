from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Destination, DestinationReview, Cruise, CruiseReview
from ..forms import DestinationReviewForm, CruiseReviewForm

def destination_reviews(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    reviews = destination.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'destinations/destination_reviews/destination_view_reviews.html', {
        'destination': destination,
        'reviews': reviews,
        'average_rating': average_rating
    })

def cruise_reviews(request, pk):
    cruise = get_object_or_404(Cruise, pk=pk)
    reviews = cruise.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'cruises/cruise_reviews/cruise_view_reviews.html', {
        'cruise': cruise,
        'reviews': reviews,
        'average_rating': average_rating
    })

@login_required
def destination_review_create(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.destination = destination
            review.name = request.user.username
            review.save()
            # Actualizar los puestos de los 3 primeros destinos por rating promedio
            top_destinations = (
                Destination.objects.annotate(avg_rating=Avg('reviews__rating'))
                .order_by('-avg_rating')[:3]
            )
            for idx, dest in enumerate(top_destinations, start=1):
                if hasattr(dest, 'position'):
                    dest.position = idx
                    dest.save(update_fields=['position'])
            messages.success(request, 'Thank you, your review has been submitted successfully!')
            return redirect('destination_details', pk=destination.pk)
    else:
        form = DestinationReviewForm()
        try:
            form.fields['name'].initial = request.user.username
            form.fields['name'].widget = forms.HiddenInput()
        except Exception:
            pass
    return render(request, 'reviews/review_create.html', {'form': form, 'item': destination, 'item_type': 'destination'})
