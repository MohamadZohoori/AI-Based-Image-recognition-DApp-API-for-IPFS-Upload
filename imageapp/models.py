from django.db import models

class UploadedImage(models.Model):
    hash = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    #user_id = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
