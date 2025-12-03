from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib import messages
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from ..models import Cruise, CruiseReview
from ..forms import CruiseReviewForm

def cruise_details(request, pk):
    cruise = get_object_or_404(Cruise, pk=pk)
    reviews = cruise.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'cruises/cruise_details.html', {
        'cruise': cruise,
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

def cruise_review_create(request, pk):
    cruise = get_object_or_404(Cruise, pk=pk)
    if request.method == 'POST':
        form = CruiseReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.cruise = cruise
            review.save()
            messages.success(request, 'Thank you, your review has been submitted successfully!')
            return redirect('cruise_details', pk=cruise.pk)
    else:
        form = CruiseReviewForm()
    return render(request, 'reviews/review_create.html', {'form': form, 'item': cruise, 'item_type': 'cruise'})

class CruiseDetailView(generic.DetailView):
    template_name = 'cruises/cruise_details.html'
    model = Cruise
    context_object_name = 'cruise'

class CruiseReviewCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'reviews/review_create.html'
    model = CruiseReview
    form_class = CruiseReviewForm
    success_message = "Thank you for your review!"