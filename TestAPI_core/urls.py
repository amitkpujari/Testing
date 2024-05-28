"""
URL configuration for TestAPI_core project.

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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from TestAPI.views import CategoryViewSet, ProductViewSet, create_excel_file_and_send_email, create_excel_file_and_send_email_in_2_min

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('generate-excel-send-email/', create_excel_file_and_send_email, name='generate_excel_send_email'),
    path('schedule-email-for-2-min/', create_excel_file_and_send_email_in_2_min, name='schedule_email_for_2_min'),
]

