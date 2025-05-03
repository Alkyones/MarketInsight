

def check_pool_and_run():
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time
    from .models import ScrapRequest, AmazonDataScrapCountry
    from django.contrib.auth.models import User
    from .functions import scrapeData
    pool = ThreadPoolExecutor(max_workers=2)
    while True:
        # Check if the pool is idle
        if pool._work_queue.empty():
            # Fetch pending requests
            pending_requests = ScrapRequest.objects.filter(status="PENDING")
            if pending_requests.exists():
                print("Pending requests found, starting scraping...")
                futures = []
                for request in pending_requests:
                    # Mark the request as "IN_PROGRESS" to avoid re-queuing
                    request.status = "IN_PROGRESS"
                    request.save()

                    # Fetch region data and user
                    regionData = AmazonDataScrapCountry.objects.get(country_code=request.country_code)
                    user = User.objects.get(id=request.user_id)

                    # Submit the task to the thread pool
                    futures.append(pool.submit(scrapeData, regionData, request._id, user))

                # Wait for all tasks to complete
                for future in as_completed(futures):
                    try:
                        future.result()  # Raise exceptions if any occurred during execution
                    except Exception as e:
                        print(f"Error occurred while processing a request: {e}")
            else:
                # If no pending requests, wait and check again
                time.sleep(10)
        else:
            # If the pool is not idle, wait and check again
            print("Pool is busy. Checking again in 10 seconds...")
            time.sleep(10)