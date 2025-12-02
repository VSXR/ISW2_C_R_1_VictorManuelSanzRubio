from django.test import TestCase
from django.core import mail
from ..models import Cruise
from ..forms import InfoRequestForm

class FormTests(TestCase):

    def setUp(self):
        self.cruise = Cruise.objects.create(name="Test Cruise", desc="...")

    def test_info_request_form_sends_email_on_save(self):
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '123456789',
            'message': 'This is a test message',
            'cruise': self.cruise.pk
        }

        form = InfoRequestForm(data=form_data)
        pass
