from django.db import models
from django.urls import reverse
from django.db.models import Avg
from decimal import Decimal
from .destination import Destination
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager
    from .review import CruiseReview


class Cruise(models.Model):
    name = models.CharField(unique=True, null=False, blank=False, max_length=70)
    desc = models.TextField(max_length=2000, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=Decimal('0.00'))
    max_capacity = models.IntegerField(null=False, blank=False, default=0)
    available_seats = models.IntegerField(null=False, blank=False, default=0)
    destinations = models.ManyToManyField(Destination, related_name='cruises')
    reviews: 'RelatedManager[CruiseReview]'  # type: ignore

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cruise_details', kwargs={"pk": self.pk})

    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    def save(self, *args, **kwargs):
        if self.available_seats > self.max_capacity:
            raise ValueError("Available seats cannot exceed maximum capacity.")
        super().save(*args, **kwargs)