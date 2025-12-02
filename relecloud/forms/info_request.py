from django import forms
from ..models import InfoRequest
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class InfoRequestForm(forms.ModelForm):
    class Meta:
        model = InfoRequest
        fields = ['name', 'email', 'phone', 'message', 'cruise']

    def save(self, commit=True):
        instance = super().save(commit=commit)
        
        if commit:                
            context = {
                'name': instance.name,
                'email': instance.email,
                'phone': instance.phone,
                'message': instance.message,
                'cruise': instance.cruise.name,
            }
            
            # Renderizamos el cuerpo del email para el administrador
            # Usamos 'info_request_email_admin.txt' como plantilla
            body = render_to_string('info_request_email_admin.txt', context)
            send_mail(
                subject=f'Nueva Solicitud de Información: {instance.name}',
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER], # Lo enviamos a 'c4relecloud@gmail.com'
                fail_silently=False,
            )
            
        return instance