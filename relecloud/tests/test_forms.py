from django.test import TestCase
from django.core import mail
from ..models import Cruise
from ..forms import InfoRequestForm

class FormTests(TestCase):
    
    def setUp(self):
        self.cruise = Cruise.objects.create(name="Test Cruise", desc="...")

    # Requisito PT1: Test de envío de email
    def test_info_request_form_sends_email_on_save(self):
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '123456789',
            'message': 'This is a test message',
            'cruise': self.cruise.pk
        }
        
        form = InfoRequestForm(data=form_data)
        self.assertTrue(form.is_valid())
    
        info_request_obj = form.save()
        self.assertEqual(len(mail.outbox), 1)
        
        sent_email = mail.outbox[0]
        self.assertIn('Nueva Solicitud de Información', sent_email.subject)
        self.assertIn('This is a test message', sent_email.body)
        self.assertIn(self.cruise.name, sent_email.body)
        self.assertEqual(sent_email.to, ['c4relecloud@gmail.com'])
        
        self.assertEqual(info_request_obj.name, 'Test User')