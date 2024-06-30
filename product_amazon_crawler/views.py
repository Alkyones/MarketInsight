from django.shortcuts import render
from django.http import HttpResponse
from .forms import AmazonCrawlerForm
from .models import AmazonDataScrapCollection
from bson import ObjectId

def scrapIndex(request):
    if request.method == 'POST':
        form = AmazonCrawlerForm(request.POST)
        if form.is_valid():
            region = form.cleaned_data['region']
            return render(request, 'amazonScrap.html', {'form': form, 'region': region})
    else:
        form = AmazonCrawlerForm()
    return render(request, 'amazonScrap.html', {'form': form})


def scrapedDataList(request):
    allData = AmazonDataScrapCollection.objects.all()
    for data in allData:
        data.id = str(data._id)
    return render(request, 'amazonScrapList.html', {'data': allData})
   
def scrapedDataDetail(request, _id):
    object_id = ObjectId(_id)
    scrapedData = AmazonDataScrapCollection.objects.get(_id=object_id)
    return render(request, 'amazonScrapDetail.html', {'categories': scrapedData.data})