from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Subscribe

class SubscribeView(APIView):
    

    def post(self, request):
        print("*"*20)
        print(request.data)
        print("*"*20)
        email = request.data.get('email')
        if email:
            Subscribe.objects.create(email=email)
        return redirect('/')
