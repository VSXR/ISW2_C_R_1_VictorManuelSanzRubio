from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Destination, DestinationReview, Purchase

class ViewTests(TestCase):

    def setUp(self):
        # Creamos destinos
        self.dest_best = Destination.objects.create(name="A (Best)", desc="...")
        self.dest_mid = Destination.objects.create(name="B (Mid)", desc="...")
        self.dest_worst = Destination.objects.create(name="C (Worst)", desc="...")
        
        # Creamos reviews para PT4
        DestinationReview.objects.create(destination=self.dest_best, rating=5)
        DestinationReview.objects.create(destination=self.dest_best, rating=5) # Avg: 5.0 (2 reviews)
        
        DestinationReview.objects.create(destination=self.dest_mid, rating=4)  # Avg: 4.0 (1 review)
        DestinationReview.objects.create(destination=self.dest_worst, rating=1) # Avg: 1.0 (1 review)

        # Creamos usuario para PT3
        self.user = User.objects.create_user(username='tester', password='testpassword')
        self.create_review_url = reverse('destination_create_reviews', kwargs={'pk': self.dest_best.pk})

    # Requisito PT4: Test de ordenación de destinos
    def test_destinations_view_sorting(self):
        response = self.client.get(reverse('destinations'))
        self.assertEqual(response.status_code, 200)
        
        # Obtenemos la variable 'top_destinations' del contexto
        top_destinations = response.context['top_destinations']
        
        expected_order = [self.dest_best, self.dest_mid, self.dest_worst]
        self.assertEqual(list(top_destinations), expected_order)

    # Requisito PT3: Test de seguridad (No logueado)
    def test_unauthenticated_user_cannot_create_review(self):
        response = self.client.get(self.create_review_url)
        
        # Debe redirigir al login
        login_url = reverse('login')
        self.assertRedirects(response, f"{login_url}?next={self.create_review_url}")

    # Requisito PT3: Test de seguridad (Logueado, SIN compra) - (TDD: Test Rojo)
    def test_authenticated_user_NO_PURCHASE_cannot_create_review(self):
        self.client.login(username='tester', password='testpassword')
        
        review_data = {'rating': 4, 'comment': 'Test comment'}
        response = self.client.post(self.create_review_url, data=review_data)
        
        # 1. No debería crear la review
        self.assertEqual(self.dest_best.reviews.count(), 2) # Siguen siendo 2, no 3
        
        # 2. Debería redirigir (p.ej. a detalles) y mostrar un mensaje de error
        self.assertRedirects(response, reverse('destination_details', kwargs={'pk': self.dest_best.pk}))
        
    # Requisito PT3: Test de seguridad (Logueado, CON compra)
    def test_authenticated_user_WITH_PURCHASE_can_create_review(self):
        # 1. Creamos la "compra" para el usuario
        Purchase.objects.create(user=self.user, destination=self.dest_best)
        
        # 2. Logueamos al usuario
        self.client.login(username='tester', password='testpassword')
        
        # 3. Enviamos la review
        review_data = {
            'name': 'Test Purchaser',
            'rating': 4,
            'comment': 'Test comment from purchaser'
        }
        response = self.client.post(self.create_review_url, data=review_data, follow=True)
        
        # 4. Comprobamos que la review se creó
        self.assertEqual(self.dest_best.reviews.count(), 3)
        self.assertTrue(DestinationReview.objects.filter(comment='Test comment from purchaser').exists())
        
        # 5. Comprobamos el mensaje de éxito
        self.assertContains(response, "Thank you for your review!")