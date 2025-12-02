from django.db import models
from django.urls import reverse
from .cruise import Cruise

class InfoRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE)

    def __str__(self):
        return f"Info request from {self.name} for {self.cruise.name}"
    
    def get_absolute_url(self):
        return reverse('info_request')