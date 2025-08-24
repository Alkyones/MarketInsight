

from celery import shared_task


@shared_task
def scrape_request_task(request_id):
    from .models import ScrapRequest, AmazonDataScrapCountry
    from django.contrib.auth.models import User
    from product_amazon_crawler.functions import scrape_data
    from bson import ObjectId
    try:
        object_id = ObjectId(request_id)
        request = ScrapRequest.objects.get(_id=object_id)
        region_data = AmazonDataScrapCountry.objects.get(country_code=request.country_code)
        user = User.objects.get(id=request.user_id)
        scrape_data(region_data, request._id, user)
        ScrapRequest.objects.filter(_id=request._id).update(status="COMPLETED")
    except Exception as e:
        print(f"Error processing request {request_id}: {e}")
        ScrapRequest.objects.filter(_id=object_id).update(status="FAILED")

@shared_task
def process_pending_requests():
    from .models import ScrapRequest
    pending_requests = ScrapRequest.objects.filter(status="PENDING")
    for request in pending_requests:
        updated = ScrapRequest.objects.filter(_id=request._id, status="PENDING").update(status="IN_PROGRESS")
        if updated:
            scrape_request_task.delay(str(request._id))