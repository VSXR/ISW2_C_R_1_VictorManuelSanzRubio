from django import forms
from ..models import DestinationReview

class DestinationReviewForm(forms.ModelForm):
    class Meta:
        model = DestinationReview
        fields = ['name', 'rating', 'comment']