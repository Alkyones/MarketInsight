from django import forms
from .models import AmazonDataScrapCountry



class AmazonCrawlerForm(forms.Form):
    region = forms.CharField(
        max_length=100,
        label="Select region",
    )
    reason = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Enter note for scraping"}),
        required=False,
        label="Reason for scraping",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import AmazonDataScrapCountry
        choices = [(e.pk, e.country_name) for e in AmazonDataScrapCountry.objects.all()]
        self.fields['region'].widget = forms.Select(choices=choices)
        self.fields['region'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter region'
        })
        self.fields['reason'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter note for scraping'
        })
        self.fields['reason'].label = ''