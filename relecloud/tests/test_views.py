from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Destination, DestinationReview, Purchase, Cruise, CruiseReview

class ViewTests(TestCase):

    def setUp(self):
        # Configuración de destinos base
        self.dest_best = Destination.objects.create(name="A (Best)", desc="...")
        self.dest_mid = Destination.objects.create(name="B (Mid)", desc="...")
        self.dest_worst = Destination.objects.create(name="C (Worst)", desc="...")
        
        # Datos para prueba de ranking (PT4)
        DestinationReview.objects.create(destination=self.dest_best, rating=5)
        DestinationReview.objects.create(destination=self.dest_best, rating=5)
        DestinationReview.objects.create(destination=self.dest_mid, rating=4)
        DestinationReview.objects.create(destination=self.dest_worst, rating=1)

        # Usuario base para pruebas de compra (PT3)
        self.user = User.objects.create_user(username='tester', password='testpassword')
        self.create_review_url = reverse('destination_create_reviews', kwargs={'pk': self.dest_best.pk})

    # Requisito PT4: Validar que los destinos se ordenan por valoración media
    def test_destinations_view_sorting(self):
        response = self.client.get(reverse('destinations'))
        self.assertEqual(response.status_code, 200)
        
        top_destinations = response.context['top_destinations']
        
        expected_order = [self.dest_best, self.dest_mid, self.dest_worst]
        self.assertEqual(list(top_destinations), expected_order)

    # Requisito PT3: Seguridad - Usuario anónimo redirigido a login
    def test_unauthenticated_user_cannot_create_review(self):
        response = self.client.get(self.create_review_url)
        
        login_url = reverse('login')
        self.assertRedirects(response, f"{login_url}?next={self.create_review_url}")

    # Requisito PT3: Seguridad - Usuario sin compra no puede dejar review
    def test_authenticated_user_NO_PURCHASE_cannot_create_review(self):
        self.client.login(username='tester', password='testpassword')
        
        review_data = {'rating': 4, 'comment': 'Test comment'}
        response = self.client.post(self.create_review_url, data=review_data)
        
        self.assertEqual(self.dest_best.reviews.count(), 2)
        self.assertRedirects(response, reverse('destination_details', kwargs={'pk': self.dest_best.pk}))
        
    # Requisito PT3: Flujo exitoso - Usuario con compra deja review
    def test_authenticated_user_WITH_PURCHASE_can_create_review(self):
        Purchase.objects.create(user=self.user, destination=self.dest_best)
        self.client.login(username='tester', password='testpassword')
        
        review_data = {
            'name': 'Test Purchaser',
            'rating': 4,
            'comment': 'Test comment from purchaser'
        }
        response = self.client.post(self.create_review_url, data=review_data, follow=True)
        
        self.assertEqual(self.dest_best.reviews.count(), 3)
        self.assertTrue(DestinationReview.objects.filter(comment='Test comment from purchaser').exists())
        self.assertContains(response, "Thank you for your review!")

    # Requisito PT3: Dependencia compleja - Review de Crucero requiere Crucero + Destino
    def test_cruise_review_restriction_logic(self):
        cruise = Cruise.objects.create(
            name="Test Cruise for Logic", 
            desc="Testing restrictions",
            price=500
        )
        cruise.destinations.add(self.dest_best)
        
        user_cruise = User.objects.create_user(username='cruise_fan', password='password')
        self.client.login(username='cruise_fan', password='password')
        
        url_create_review = reverse('cruise_create_reviews', kwargs={'pk': cruise.pk})
        
        review_data = {
            'name': 'Cruise Fan', 
            'rating': 5, 
            'comment': 'Amazing experience!'
        }

        # CASO A: Usuario tiene Crucero pero NO el Destino (Debe fallar)
        Purchase.objects.create(user=user_cruise, cruise=cruise)
        
        response = self.client.post(url_create_review, data=review_data)
        
        self.assertFalse(CruiseReview.objects.filter(comment='Amazing experience!').exists())
        
        expected_url = reverse('cruise_details', kwargs={'pk': cruise.pk})
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)
        
        response_target = self.client.get(expected_url)
        messages = list(response_target.context['messages'])
        self.assertTrue(any("You must purchase the destination" in str(m) for m in messages))

        # CASO B: Usuario adquiere el Destino (Ahora tiene ambos -> Debe funcionar)
        Purchase.objects.create(user=user_cruise, destination=self.dest_best)
        
        response = self.client.post(url_create_review, data=review_data, follow=True)
        
        self.assertTrue(CruiseReview.objects.filter(comment='Amazing experience!').exists())
        self.assertContains(response, "Thank you")
