from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from ..models import Destination, DestinationReview, Purchase
from ..forms import DestinationReviewForm
from django.contrib.auth.decorators import login_required

def destinations(request):
    # Top 3 destinos por media de reviews y, en caso de empate, por cantidad de reviews
    top_destinations = Destination.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
    ).order_by('-avg_rating', '-num_reviews')[0:3]
    return render(request, 'destinations/destinations.html', {
        'top_destinations': top_destinations
    })

def show_all_destinations(request):
    all_destinations = Destination.objects.all()
    return render(request, 'destinations/destination_in_detail/destination_view_all.html', {'destinations': all_destinations})

def destination_details(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    reviews = destination.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Para saber si el usuario ha comprado este destino y dejarle hacer una review
    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = Purchase.objects.filter(
            user=request.user, 
            destination=destination
        ).exists()

    return render(request, 'destinations/destination_in_detail/destination_details.html', {
        'destination': destination,
        'reviews': reviews,
        'average_rating': average_rating,
        'has_purchased': has_purchased,
    })

class DestinationUpdateView(generic.UpdateView):
    template_name = 'destinations/destination_confirm/destination_confirm_edit.html'
    model = Destination
    fields = ['name', 'image_url', 'desc']

class DestinationDeleteView(generic.DeleteView):
    template_name = 'destinations/destination_confirm/destination_confirm_delete.html'
    model = Destination
    success_url = reverse_lazy('destinations')

# Requisito PT3: Vista de creación de Review modificada
class DestinationReviewCreate(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'reviews/review_create.html'
    model = DestinationReview
    form_class = DestinationReviewForm
    success_message = "Thank you for your review!"

    def dispatch(self, request, *args, **kwargs):
        # 1. Comprobar si el usuario está autenticado (es lo que hace LoginRequiredMixin)
        if not request.user.is_authenticated:
            # Con handle_no_permission() redirigimos al login
            return self.handle_no_permission()

        # 2. Si SÍ está autenticado, obtenemos el destino
        self.destination = get_object_or_404(Destination, pk=self.kwargs['pk'])
        
        # 3. Comprobar si ha comprado este destino
        has_purchased = Purchase.objects.filter(
            user=request.user, 
            destination=self.destination
        ).exists()
        
        if not has_purchased:
            messages.error(request, "You must purchase this trip to review it.")
            return redirect('destination_details', pk=self.destination.pk)
        
        # 4. Si está autenticado Y ha comprado, continuar a la vista
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destination'] = self.destination
        context['item'] = self.destination
        context['item_type'] = 'destination'
        return context

    def form_valid(self, form):
        # Asignar el destino y el usuario (o nombre) antes de guardar
        form.instance.destination = self.destination
        if 'name' not in form.cleaned_data or not form.cleaned_data['name']:
            form.instance.name = self.request.user.username
        
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir de vuelta a los detalles del destino
        return reverse('destination_details', kwargs={'pk': self.destination.pk})

@login_required
def purchase_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    
    # Usa get_or_create para evitar compras duplicadas
    purchase, created = Purchase.objects.get_or_create(
        user=request.user, 
        destination=destination
    )
    
    if created:
        messages.success(request, f"You have successfully purchased a trip to {destination.name}!")
    else:
        messages.info(request, f"You have already purchased a trip to {destination.name}.")
        
    return redirect('destination_details', pk=pk)