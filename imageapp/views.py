import ipfshttpclient
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .models import UploadedImage
import mimetypes
from django.core.files.storage import FileSystemStorage
from .tasks import remove_photo
from datetime import datetime, timedelta
import os 
from django.conf import settings
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

class ImageUploadView(APIView):
    def post(self, request, format=None):
        image = request.FILES['image']  # Assuming the image file is sent as 'image' in the request

        
        # Get the MIME type of the uploaded file
        mime_type, _ = mimetypes.guess_type(image.name)

        # Check if the MIME type is an image
        if mime_type and mime_type.startswith('image/'):
            max_file_size = 10 * 1024 * 1024  # Maximum file size in bytes (e.g., 10 MB)
            
            if image.size <= max_file_size:

                ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')  # Connect to the IPFS daemon

                print(image.name)
                # Store the image on IPFS
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                image.name = f'{timestamp}.jpg'  # Update the extension based on the actual file type
                fs = FileSystemStorage(location='temp')
                saved_image = fs.save(image.name, image)
                temp_file_path = os.path.join(BASE_DIR, 'temp', image.name)
                remove_photo.apply_async(args=[temp_file_path], eta=datetime.now() + timedelta(minutes=60))
                
                print(image.name)

                res = ipfs_client.add(image)

                print(res)
                image_hash = res['Hash']

                uploaded_image = UploadedImage.objects.create(
                    hash=image_hash,
                    name=image.name,
                    size=image.size,  # Save the size of the image
                    #user_id=request.user.id,  # Save the user ID (assuming authentication is implemented)
                    uploaded_at=datetime.now()  # Save the current date and time
                )
        
                # Return the IPFS hash in the response
                return Response({'ipfs_hash': image_hash})
            else:
                return HttpResponse('{"status": false, "message": "File size exceeds the maximum limit."}', content_type='application/json')
        else:
            # Return a response indicating that the file is not a photo
            return HttpResponse('{"status": false, "message": "Invalid file format. Only image files are allowed."}', content_type='application/json')














"""

from django.http import HttpResponse
import ipfshttpclient

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

        try:
            # Add image data to IPFS
            res = ipfs_client.add(image.read())
            # 'res' will contain the response from IPFS, including the hash of the uploaded image

            # Handle the response as desired (e.g., store the hash in your database)
            image_hash = res['Hash']
            # You can now use the image_hash for further processing or retrieval

            # Return a success response
            return HttpResponse(f'Image uploaded successfully. IPFS hash: {image_hash}')
        except ipfshttpclient.exceptions.ErrorResponse as e:
            # Handle IPFS-related errors
            return HttpResponse(f'Error uploading image to IPFS: {str(e)}', status=500)
    
    # Return an error response if the request method is not POST or no image is provided
    return HttpResponse('Invalid request', status=400)
"""