from django.db import models
from .destination import Destination
from .cruise import Cruise

class DestinationReview(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100, default='Anonymous', null=False, blank=False)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    def __str__(self):
        truncated_comment = (self.comment[:30] + "...") if len(self.comment) > 30 else self.comment
        return f"Review for {self.destination.name}: {self.rating} stars ({truncated_comment})"

class CruiseReview(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100, default='Anonymous', null=False, blank=False)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    def __str__(self):
        truncated_comment = (self.comment[:30] + "...") if len(self.comment) > 30 else self.comment
        return f"Review for {self.cruise.name}: {self.rating} stars ({truncated_comment})"