from django.test import TestCase
from ..models import Destination, DestinationReview, Cruise, CruiseReview

class ModelTests(TestCase):
    def setUp(self):
        self.dest = Destination.objects.create(
            name="Testeo de Destino: Testeo",
            image_url="https://example.com/marte.jpg",
            desc="El planeta rojo."
        )
        self.cruise = Cruise.objects.create(
            name="Testeo de Crucero: Viaje a la Luna",
            desc="Un crucero rápido."
        )

    def test_destination_model_saves_image_url(self):
        dest_guardado = Destination.objects.get(name="Testeo de Destino: Testeo")
        self.assertEqual(dest_guardado.image_url, "https://example.com/marte.jpg")
        self.assertEqual(dest_guardado.desc, "El planeta rojo.")

    def test_destination_average_rating(self):
        self.assertEqual(self.dest.average_rating(), 0)
        DestinationReview.objects.create(destination=self.dest, rating=5, comment="...")
        DestinationReview.objects.create(destination=self.dest, rating=1, comment="...")
        self.assertEqual(self.dest.average_rating(), 3.0)

    def test_cruise_average_rating(self):
        self.assertEqual(self.cruise.average_rating(), 0)
        CruiseReview.objects.create(cruise=self.cruise, rating=4, comment="...")
        CruiseReview.objects.create(cruise=self.cruise, rating=4, comment="...")
        self.assertEqual(self.cruise.average_rating(), 4.0)
