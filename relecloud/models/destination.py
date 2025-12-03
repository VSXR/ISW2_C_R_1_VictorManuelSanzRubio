from django.db import models
from django.urls import reverse
from django.db.models import Avg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager
    from .review import DestinationReview

class Destination(models.Model):
    name = models.CharField(unique=True, null=False, blank=False, max_length=50)
    image_url = models.URLField(max_length=200, null=False, blank=False) # agregar DEFAULT para poner una imagen predeterminada
    desc = models.TextField(max_length=2000, null=False, blank=False)
    reviews: 'RelatedManager[DestinationReview]'  # type: ignore
    position = models.PositiveIntegerField(default=0)  # <-- Añadido

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('destination_details', kwargs={"pk": self.pk})

    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0