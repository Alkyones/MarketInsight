

from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def fetch_and_mark_pending_requests():
    from .models import ScrapRequest
    marked_requests = []
    pending_requests = ScrapRequest.objects.filter(status="PENDING")
    for request in pending_requests:
        updated = ScrapRequest.objects.filter(_id=request._id, status="PENDING").update(status="IN_PROGRESS")
        if updated:
            marked_requests.append(request)
        else:
            print(f"Request {request._id} was already picked up by another worker.")
    return marked_requests

def get_region_and_user(request):
    try:
        from .models import AmazonDataScrapCountry
        from django.contrib.auth.models import User
        region_data = AmazonDataScrapCountry.objects.get(country_code=request.country_code)
        user = User.objects.get(id=request.user_id)
        return region_data, user
    except Exception as e:
        print(f"Error fetching region/user for request {request._id}: {e}")
        return None, None

def process_requests(pool, requests):
    from product_amazon_crawler.functions import scrape_data
    futures = []
    for request in requests:
        region_data, user = get_region_and_user(request)
        if not region_data or not user:
            continue
        futures.append(pool.submit(scrape_data, region_data, request._id, user))
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error occurred while processing a request: {e}")
            print("Shutting down pool due to error.")
            pool.shutdown(wait=False)
            return False
    return True

def check_pool_and_run():
    with ThreadPoolExecutor(max_workers=1) as pool:
        while True:
            if pool._work_queue.empty():
                marked_requests = fetch_and_mark_pending_requests()
                if marked_requests:
                    print("Pending requests found, starting scraping...")
                    success = process_requests(pool, marked_requests)
                    if not success:
                        return
                else:
                    time.sleep(10)
            else:
                print("Pool is busy. Checking again in 10 seconds...")
                time.sleep(10)