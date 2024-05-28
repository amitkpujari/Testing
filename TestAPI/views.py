import json
from time import sleep
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.conf import settings
from celery import shared_task
import os
import openpyxl
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.cache import cache
from django.core.serializers import serialize

logger = logging.getLogger(__name__)

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        cached_products = cache.get('all_products')
        
        if cached_products is None:
            products = Product.objects.all()
            serialized_products = serialize('json', products)
            cache.set('all_products', serialized_products)
        else:
            products = Product.objects.all()  # Convert the serialized data back to a queryset
        
        return products
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

@shared_task
def generate_and_send_excel_file(email):
    try:
        users = User.objects.all()
        excel_file_path = generate_excel_file(users)
        send_email_with_attachment(email, 'Excel File', 'Please see attached Excel file.', excel_file_path)
        os.remove(excel_file_path)
        logger.info(f"Email sent successfully to {email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

        
@shared_task
def waiting(duration):
    sleep(duration)
    return None

def send_email_with_attachment(to_email, subject, body, attachment_path):
    try:
        email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [to_email])
        email.attach_file(attachment_path)
        email.send()
    except Exception as e:
        logger.error(f"Failed to send email with attachment: {e}")

def generate_excel_file(users):
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['ID', 'Name', 'Is Active'])
        for user in users:
            ws.append([user.id, user.username, user.is_active])
        excel_file_path = 'users.xlsx'
        wb.save(excel_file_path)
        return excel_file_path
    except Exception as e:
        logger.error(f"Failed to generate Excel file: {e}")

@csrf_exempt
def create_excel_file_and_send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        generate_and_send_excel_file.delay(email)
        return JsonResponse({'message': 'Email with Excel file is being sent.'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'})

@csrf_exempt
def create_excel_file_and_send_email_in_2_min(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        generate_and_send_excel_file.apply_async(args=[email], countdown=120)
        return JsonResponse({'message': 'Email with Excel file will be sent after 2 minutes.'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'})
    