
from django import forms
from enum import Enum

class CountryEnum(Enum):
    AU = {"country": "Australia", "url": "https://www.amazon.com.au"}
    AE = {"country": "United Arab Emirates", "url": "https://www.amazon.ae"}
    BR = {"country": "Brazil", "url": "https://www.amazon.com.br"}
    CA = {"country": "Canada", "url": "https://www.amazon.ca"}
    CN = {"country": "China", "url": "https://www.amazon.cn"}
    DE = {"country": "Germany", "url": "https://www.amazon.de"}
    ES = {"country": "Spain", "url": "https://www.amazon.es"}
    FR = {"country": "France", "url": "https://www.amazon.fr"}
    IN = {"country": "India", "url": "https://www.amazon.in"}
    IT = {"country": "Italy", "url": "https://www.amazon.it"}
    JP = {"country": "Japan", "url": "https://www.amazon.co.jp"}
    MX = {"country": "Mexico", "url": "https://www.amazon.com.mx"}
    SG = {"country": "Singapore", "url": "https://www.amazon.sg"}
    TR = {"country": "Turkey", "url": "https://www.amazon.com.tr"}
    UK = {"country": "United Kingdom", "url": "https://www.amazon.co.uk"}
    US = {"country": "United States", "url": "https://www.amazon.com"}

    @property
    def country(self):
        return self.value["country"]

    @property
    def url(self):
        return self.value["url"]


class AmazonCrawlerForm(forms.Form):
    region = forms.CharField(
        max_length=100,
        widget=forms.Select(choices=[(e.url, e.country) for e in CountryEnum])
    )
