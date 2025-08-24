# MarketInsight Product Scraping Platform
Django Based Web Application For Automating Scraping Data
- Multi browser support (Chrome Native)
- Quick access to user scrap requests and scraped data.
- Two step authentication for better privacy.
- Manipulation over Scraped Data.
- Stylized User Interface for better experience.
- Threading for handling multiple scrap processes.

# V2 Release
- Scraping stabilised
- Thread removed and Celery implemented.
- Required files for docker has been added to the project.

# Upcoming Releases
- Local marketplace's integration (Ebay, Hepsiburada)
- Major upgrade in UI.
- Better visibility over scraped data.
- Safari support for Apple users.
- Token system for premium scraps.
- Premium scraps that allows users to scrap the data the way they want and reshape on flight.
- Excel export for scraped data.
- Different scraping methods for getting different kind of data for user needs.

  
# How to Run the Project


1. **Create and activate a virtual environment (recommended):**
	```bash
	python -m venv venv
	source venv/bin/activate  # On Windows: venv\Scripts\activate
	```

3. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```

4. **Apply migrations:**
	```bash
	python manage.py migrate
	```

5. **Create a superuser (optional, for admin access):**
	```bash
	python manage.py createsuperuser
	```

6. **Run the development server:**
	```bash
	python manage.py runserver
	```

# How to Test

To run the test suite and ensure everything is working as expected:

```bash
python manage.py test
```

You can also run tests for a specific app:

```bash
python manage.py test <app_name>
```

Replace `<app_name>` with `accounts`, `main_page`, or `product_amazon_crawler` as needed.

# Main Page
- Main page allows users to navigate through platform easily, here they can go to check their scrap requests, their status, and scraped data's detail.
![preview](/static/assets/main_page.png)

# Scrap Requests
- Page allows users to create new scrap request on selected platform
![preview](/static/assets/new_scrap_request.png)
- User also can check its ongoing scraps and their statuses on listing.
![preview](/static/assets/scrap_requests.png)

# Scraped Data
- Page allows users to see scraped data and its details.
![preview](/static/assets/scraped_data_list.png)
- User also can check its details clicking the details button on the list.
![preview](/static/assets/scraped_data_detail_list.png)
![preview](/static/assets/scraped_data_detail_list_open.png)
