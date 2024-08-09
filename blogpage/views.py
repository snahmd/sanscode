from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Subscribe

class SubscribeView(APIView):
    

    def post(self, request):
        print(request.data)
        email = request.data.get('email')
        if email:
            Subscribe.objects.create(email=email)
        return redirect('/')
