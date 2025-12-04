from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib import messages
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from ..models import Cruise, CruiseReview, Purchase
from ..forms import CruiseReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse

def cruise_details(request, pk):
    cruise = get_object_or_404(Cruise, pk=pk)
    reviews = cruise.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    has_purchased_cruise = False
    has_purchased_destination = False
    
    if request.user.is_authenticated:
        # 1. Comprobar compra del crucero
        has_purchased_cruise = Purchase.objects.filter(
            user=request.user, 
            cruise=cruise
        ).exists()
        
        # 2. Comprobar compra de CUALQUIERA de los destinos del crucero
        # Filtramos si existe alguna compra del usuario cuyo destino esté en la lista de destinos de este crucero
        has_purchased_destination = Purchase.objects.filter(
            user=request.user,
            destination__in=cruise.destinations.all()
        ).exists()

    return render(request, 'cruises/cruise_details.html', {
        'cruise': cruise,
        'reviews': reviews,
        'average_rating': average_rating,
        'has_purchased_cruise': has_purchased_cruise,           # Nueva variable
        'has_purchased_destination': has_purchased_destination, # Nueva variable
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
def cruise_review_create(request, pk):
    cruise = get_object_or_404(Cruise, pk=pk)
    
    # 1. Verificar crucero
    has_purchased_cruise = Purchase.objects.filter(
        user=request.user, 
        cruise=cruise
    ).exists()
    
    if not has_purchased_cruise:
        messages.error(request, "You must purchase this cruise to review it.")
        return redirect('cruise_details', pk=pk)

    # 2. Verificar destino
    has_purchased_destination = Purchase.objects.filter(
        user=request.user,
        destination__in=cruise.destinations.all()
    ).exists()

    if not has_purchased_destination:
        messages.error(request, "You must purchase the destination of this cruise to review it.")
        # Redirigimos al detalle del crucero (allí verá el botón para comprar destino)
        return redirect('cruise_details', pk=pk)

    # Si pasa ambas comprobaciones, procesar formulario
    if request.method == 'POST':
        form = CruiseReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.cruise = cruise
            review.name = request.user.username
            review.save()
            messages.success(request, 'Thank you, your review has been submitted successfully!')
            return redirect('cruise_details', pk=cruise.pk)
    else:
        form = CruiseReviewForm()
        
    return render(request, 'reviews/review_create.html', {
        'form': form, 
        'item': cruise, 
        'item_type': 'cruise'
    })

@login_required
def purchase_cruise(request, pk):
    cruise = get_object_or_404(Cruise, pk=pk)
    
    # Crear la compra si no existe (Purchase vincula usuario y crucero)
    purchase, created = Purchase.objects.get_or_create(
        user=request.user, 
        cruise=cruise
    )
    
    if created:
        messages.success(request, f"You have successfully purchased a ticket for {cruise.name}!")
    else:
        messages.info(request, f"You have already purchased a ticket for {cruise.name}.")
        
    # Redirigir de vuelta a los detalles del crucero
    return redirect('cruise_details', pk=pk)



class CruiseDetailView(generic.DetailView):
    template_name = 'cruises/cruise_details.html'
    model = Cruise
    context_object_name = 'cruise'

class CruiseReviewCreate(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'reviews/review_create.html'
    model = CruiseReview
    form_class = CruiseReviewForm
    success_message = "Thank you for your review!"

    def dispatch(self, request, *args, **kwargs):
        # Comprobar si el usuario está autenticado
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Obtener el crucero usando la PK de la URL
        self.cruise = get_object_or_404(Cruise, pk=self.kwargs['pk'])
        
        # Comprobar si ha comprado este crucero (usando el modelo Purchase)
        has_purchased = Purchase.objects.filter(
            user=request.user, 
            cruise=self.cruise
        ).exists()
        
        if not has_purchased:
            messages.error(request, "You must purchase this cruise to review it.")
            return redirect('cruise_details', pk=self.cruise.pk)
        
        # Si todo es correcto, continuar
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cruise'] = self.cruise
        context['item'] = self.cruise
        context['item_type'] = 'cruise'
        return context

    def form_valid(self, form):
        # Asignar el crucero y el usuario antes de guardar
        form.instance.cruise = self.cruise
        if 'name' not in form.cleaned_data or not form.cleaned_data['name']:
            form.instance.name = self.request.user.username
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir a los detalles del crucero tras crear la review
        return reverse('cruise_details', kwargs={'pk': self.cruise.pk})