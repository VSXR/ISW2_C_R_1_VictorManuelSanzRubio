from django.test import TestCase
from ..models import Cruise

class FormTests(TestCase):

    def setUp(self):
        self.cruise = Cruise.objects.create(name="Test Cruise", desc="...")
