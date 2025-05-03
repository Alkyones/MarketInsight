from django.shortcuts import render, redirect
from django.http import JsonResponse
from.forms import AmazonCrawlerForm
from.models import AmazonDataScrapCollection, ScrapRequest
from bson import ObjectId
from.functions import *
from concurrent.futures import ThreadPoolExecutor
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import serialize

@login_required
def scrap_index(request):
    user_instance = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = AmazonCrawlerForm(request.POST)
        if form.is_valid():
            region_url = form.cleaned_data['region']
            print(region_url)
            scrap_request = ScrapRequest(country_code=region_url, user=user_instance)
            scrap_request.save()
            future = ThreadPoolExecutor(max_workers=1).submit(scrapeData, region_url, scrap_request._id, user_instance)
            return redirect('amazon:request-list')
    else:
        form = AmazonCrawlerForm()
    return render(request, 'amazonScrap.html', {'form': form})

@login_required
def scrap_requests_list(request):
    scrap_requests = ScrapRequest.objects.filter(user=request.user)
    for scrap_request in scrap_requests:
        scrap_request.id = str(scrap_request._id)
        
    return render(request, 'amazonScrapRequestList.html', {'scrap_requests': scrap_requests})

def get_scrap_request_status(request, pk):
    scrap_request = ScrapRequest.objects.get(_id=ObjectId(pk))
    return JsonResponse({'status': scrap_request.status})

@login_required
def scraped_data_list(request):
    request_user = User.objects.get(id=request.user.id)
    all_data = AmazonDataScrapCollection.objects.filter(user=request_user)
    for data in all_data:
        data.id = str(data._id)
        print(data)
    return render(request, 'amazonScrapList.html', {'data': all_data})

@login_required
def scraped_data_detail(request, _id):
    object_id = ObjectId(_id)
    scraped_data = AmazonDataScrapCollection.objects.get(_id=object_id, user=request.user)
    return render(request, 'amazonScrapDetail.html', {'categories': scraped_data.data})


@login_required
def scraped_data_detail_json(request, _id):
    object_id = ObjectId(_id)
    scraped_data = AmazonDataScrapCollection.objects.get(_id=object_id, user=request.user)
    serializer = serialize('json', scraped_data.data)
    return JsonResponse(serializer)