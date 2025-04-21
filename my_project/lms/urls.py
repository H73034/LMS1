from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   path('add_course/', views.add_course, name='add_course'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    # other URLs...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development