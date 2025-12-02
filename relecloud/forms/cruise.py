from django import forms
from ..models import CruiseReview

class CruiseReviewForm(forms.ModelForm):
    class Meta:
        model = CruiseReview
        fields = ['name', 'rating', 'comment']