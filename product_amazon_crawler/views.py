from django.shortcuts import render, redirect
from django.http import JsonResponse
from.forms import AmazonCrawlerForm
from.models import AmazonDataScrapCollection, ScrapRequest
from bson import ObjectId
from.functions import *
from concurrent.futures import ThreadPoolExecutor
import json
def scrap_index(request):
    if request.method == 'POST':
        form = AmazonCrawlerForm(request.POST)
        if form.is_valid():
            region_url = form.cleaned_data['region']
            scrap_request = ScrapRequest(country_code=region_url)
            scrap_request.save()
            future = ThreadPoolExecutor(max_workers=1).submit(scrapeData, region_url, scrap_request.id)
            return redirect('request-list')
    else:
        form = AmazonCrawlerForm()
    return render(request, 'amazonScrap.html', {'form': form})

def scrap_requests_list(request):
    scrap_requests = ScrapRequest.objects.all()
    return render(request, 'amazonScrapRequestList.html', {'scrap_requests': scrap_requests})

def get_scrap_request_status(request, pk):
    scrap_request = ScrapRequest.objects.get(pk=pk)
    return JsonResponse({'status': scrap_request.status})

def scraped_data_list(request):
    all_data = AmazonDataScrapCollection.objects.all()
    for data in all_data:
        data.id = str(data._id)
    return render(request, 'amazonScrapList.html', {'data': all_data})

def scraped_data_detail(request, _id):
    object_id = ObjectId(_id)
    scraped_data = AmazonDataScrapCollection.objects.get(_id=object_id)
    return render(request, 'amazonScrapDetail.html', {'categories': scraped_data.data})