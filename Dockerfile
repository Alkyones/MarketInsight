
# Dockerfile for Django + Chromium (no MongoDB)
FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies and Chromium
RUN apt-get update && \
	apt-get install -y wget curl gnupg2 gcc libpq-dev build-essential unzip chromium chromium-driver && \
	rm -rf /var/lib/apt/lists/*

# Symlink for Selenium compatibility
RUN ln -s /usr/bin/chromium /usr/bin/chromium-browser

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /code/

# Collect static files (optional, if you use staticfiles)
# RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
