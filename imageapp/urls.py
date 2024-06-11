from django.urls import path
from imageapp import views

urlpatterns = [
    path('upload/', views.ImageUploadView.as_view(), name='image-upload'),
]