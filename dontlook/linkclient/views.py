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
import json
import re
from ..mayanDB import MayanDatabaseConnection

# import json
# json.dumps()

# Get an instance of a logger
logger = logging.getLogger(__name__)
# logger.exception()
# logger.error()
# logger.critical()

mayan_database = MayanDatabaseConnection()

@api_view()
def index_route(request):
	logger.debug("Logger error")
	return Response({"message": "It is the mayan/Aims supporting API."})


@api_view(['GET', 'POST'])
def link_client(request, policy_number):
	# Removing slashes from policy_number
	# policy_number = result = re.sub('[^0-9]','', policy_number)

	if (request.method == 'POST'):
		policy_number = request.data.get('policy_number')
		if (len(policy_number) == 17):
			string_list = [policy_number[i] for i in range(0, 17)]
			string_list.insert(13, "/")
			string_list.insert(7, "/")
			string_list.insert(6, "/")
			string_list.insert(3, "/")
			new_policy_number = "".join(string_list)
			logger.info(f"Updating policy_number {policy_number} to {new_policy_number}")
			# TODO Update metadata in DB. by metadata_id=2 & document_id
			policy_number = new_policy_number

		# '010/030/1/000110/2020'
		result = mayan_database.get_doc_id_by_policy_no(policy_number)
		if not result.get('document_id'):
			return Response({"message": "Request failed! Metadata id not found"}, 404)

		# TODO query for the client id in AIMs
		client_id = '00123'
		metatype_id = 5

		result = mayan_database.insert_metadata_by_policy_no({
			'metatype_id': metatype_id,
			'client_id': client_id,
			'document_id': result.get('document_id')
		})
		if not result:
			return Response({"message": "Update db query failed!"}, 400)

		return Response({"message": "Got some POST data!", "data": policy_number})

	return Response({
		"query param id": policy_number,
		"message": "Make a post with a 'policy_number' to link to the client in AIMs."
	})
