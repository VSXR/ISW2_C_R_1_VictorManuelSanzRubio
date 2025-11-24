from django.db import models 
from django.urls import reverse # Import reverse to use get_absolute_url (line 20)

# Create your models here.
# DESTINATION MODEL
class Destination(models.Model):
    def __str__(self): # Metodo para mostrar el nombre del destino en el admin
        return self.name
    
    def get_absolute_url(self): # Metodo para redirigir a la pagina de detalle del destino
        return reverse('destination_detail', kwargs={"pk": self.pk}) # Redirige a la pagina de detalle del destino
    
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=50
    )
    desc = models.TextField(
        max_length=2000, 
        null=False,
        blank=False
    )

# CRUISE MODEL
class Cruise(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(
        unique= True,
        null= False,
        blank= False,
        max_length= 70,
    )
    desc = models.TextField(
        max_length= 2000, 
        null= False,
        blank= False
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name= 'cruises'
    )

# INFO REQUEST MODEL
class InfoRequest(models.Model):
    name = models.CharField(
        max_length=70, 
        null=False, 
        blank=False
    )
    email = models.EmailField(
        blank=False,
        null=False
    )
    phone = models.CharField(
        max_length=15,
        blank=False, 
        null=False
    )
    message = models.TextField(
        max_length=2000, 
        blank=False, 
        null=False
    )
    cruise = models.ForeignKey(
        Cruise, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True
    )

