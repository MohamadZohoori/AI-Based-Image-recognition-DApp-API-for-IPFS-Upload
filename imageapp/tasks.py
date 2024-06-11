
"""
from celery import shared_task
from datetime import timedelta
from django.conf import settings
import os


@shared_task
def clean_photos():
    # Define the path to the directory where the photos are stored
    photo_directory = os.path.join(settings.BASE_DIR, 'temp')

    # Iterate over the files in the directory
    for filename in os.listdir(photo_directory):
        file_path = os.path.join(photo_directory, filename)
        modified_time = os.path.getmtime(file_path)

        # Calculate the time difference in seconds
        time_difference = timedelta(seconds=settings.PHOTO_CLEANUP_TIME)

        # Check if the file has exceeded the time threshold
        if modified_time + time_difference.total_seconds() < time.time():
            # Delete the file
            os.remove(file_path)
"""

from celery import shared_task
import os
from datetime import datetime, timedelta

@shared_task
def remove_photo(photo_path):
    # Calculate the timestamp 1 hour from now
    expiry_time = datetime.now() + timedelta(minutes=60)

    # Check if the photo exists and its modification time is older than the expiry time
    if os.path.exists(photo_path):
        modified_time = datetime.fromtimestamp(os.path.getmtime(photo_path))
        if modified_time < expiry_time:
            os.remove(photo_path)