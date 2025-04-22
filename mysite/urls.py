# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin login URL
    path('', include('lms.urls')),  # Your app URLs
    path('course/<int:course_id>/', include('lms.urls')),
    # other URLs...
]
