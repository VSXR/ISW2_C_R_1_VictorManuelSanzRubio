from django.test import TestCase
from ..models import Destination, DestinationReview, Cruise, CruiseReview

class ModelTests(TestCase):

    def setUp(self):
        # Creamos los objetos una vez para todos los tests de esta clase
        self.dest = Destination.objects.create(
            name="Testeo de Destino: Testeo",
            image_url="https://example.com/marte.jpg",
            desc="El planeta rojo."
        )
        self.cruise = Cruise.objects.create(
            name="Testeo de Crucero: Viaje a la Luna",
            desc="Un crucero rápido."
        )

    # Requisito PT2: Test de imagen en Destination
    def test_destination_model_saves_image_url(self):
        # 1. Buscamos el objeto por el nombre exacto creado en setUp
        dest_guardado = Destination.objects.get(name="Testeo de Destino: Testeo")
        
        # 2. Comprobamos los campos
        self.assertEqual(dest_guardado.image_url, "https://example.com/marte.jpg")
        self.assertEqual(dest_guardado.desc, "El planeta rojo.")

    # Requisito PT3: Test de valoración media (Destinos)
    def test_destination_average_rating(self):
        # 1. Sin reviews, la media debe ser 0
        self.assertEqual(self.dest.average_rating(), 0)
        
        # 2. Añadimos reviews
        DestinationReview.objects.create(destination=self.dest, rating=5, comment="...")
        DestinationReview.objects.create(destination=self.dest, rating=1, comment="...")
        
        # 3. La media debe ser (5+1)/2 = 3.0
        self.assertEqual(self.dest.average_rating(), 3.0)

    # Requisito PT3: Test de valoración media (Cruceros)
    def test_cruise_average_rating(self):
        # 1. Sin reviews, la media debe ser 0
        self.assertEqual(self.cruise.average_rating(), 0)
        
        # 2. Añadimos reviews
        CruiseReview.objects.create(cruise=self.cruise, rating=4, comment="...")
        CruiseReview.objects.create(cruise=self.cruise, rating=4, comment="...")
        
        # 3. La media debe ser (4+4)/2 = 4.0
        self.assertEqual(self.cruise.average_rating(), 4.0)