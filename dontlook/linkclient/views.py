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
import logging
import re

# import json
# json.dumps()

# Get an instance of a logger
logger = logging.getLogger(__name__)
# logger.debug()
# logger.info()
# logger.warning()
# logger.error()
# logger.critical()

# Function Based Views
# @api_view()

@api_view()
def index_route(request):
    return Response({"message": "It is the mayan/Aims supporting API."})

@api_view(['GET', 'POST'])
def link_client(request, policy_number):
	# initialLength = len(policy_number)
	# policy_number = result = re.sub('[^0-9]','', policy_number)

	if (request.method == 'POST') and (len(request.data.policy_number) == 17):
		# print(f'foo.{s}.baz)'
		string_list = request.data.policy_number.split()
		string_list.insert(14, "/")
		string_list.insert(8, "/")
		string_list.insert(7, "/")
		string_list.insert(4, "/")
		new_policy_number = string_list.join()
		logger.debug(f"Updating policy_number {request.data.policy_number} to {new_policy_number}")
		## TODO Update metadata in DB. by metadata_id=2 & document_id
		policy_number = new_policy_number


	## TODO query for the client id
	## TODO attach id as metadata to document
	if request.method == 'POST':
		return Response({"message": "Got some POST data!", "data": request.data})

    return Response({"query param id": new_policy_number})

# from rest_framework.views import APIView
# class WelcomeMessage(APIView):
#     def get(self, request):
#         return Response({"Index": "Welcome"})
