# >>> requests.post('https://httpbin.org/post', data={'key':'value'})
# >>> requests.put('https://httpbin.org/put', data={'key':'value'})
# >>> requests.delete('https://httpbin.org/delete')
# >>> requests.head('https://httpbin.org/get')
# >>> requests.patch('https://httpbin.org/patch', data={'key':'value'})
# >>> requests.options('https://httpbin.org/get')

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
# import json
# json.dumps()

# Function Based Views
# @api_view()

@api_view()
def indexroute(request):
    return Response({"message": "It is the mayan/Aims supporting API."})

@api_view(['GET', 'POST'])
def linktheclient(request, id):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"id": id})

# from rest_framework.views import APIView
# class WelcomeMessage(APIView):
#     def get(self, request):
#         return Response({"Index": "Welcome"})
