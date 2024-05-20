"""
URL configuration for RKFinanceApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('contact/', contact, name='contact'),
    path('contact/home/', home, name='contact'),
    path('home/', home, name='contact'),
    path('save/data/', save_data, name='save_data'),
    path('contact/home/save/data/', save_data, name='save_data'),
    path('home/save/data/', save_data, name='save_data'),
    path('feedback', feedback, name='feedback'),
    path('save/feedback/', save_feedback, name='feedback'),
    path('get/feedback/', get_feedback, name='feedback'),
    path('display_feedback/', display_feedback, name='feedback'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)