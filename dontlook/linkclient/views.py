from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import logging
import json
import re
import os
import time
import socket
import sys
from ..mayanDB import MayanDatabaseConnection

# json.dumps()
CLIENTS_CABINET_ID = 58
AUTH=(os.environ.get("MAYAN_APP_USER_NAME"), os.environ.get("MAYAN_APP_USER_PASS"))

mayan_app_host = os.environ.get("MAYAN_APP_HOST")
logger = logging.getLogger(__name__)

def print_a_log(msg):
	print(f"\nError: {msg}")
	logger.critical(f'\n\n{msg}\n\n')

mayan_database = MayanDatabaseConnection()
metatype_id = mayan_database.get_client_no_metatype_id()
if not metatype_id:
	exit(3)


def alter_policy_number(policy_number):
	# Removing slashes from policy_number
	# policy_number = result = re.sub('[^0-9]','', policy_number)

	string_list = [policy_number[i] for i in range(0, 17)]
	string_list.insert(13, "/")
	string_list.insert(7, "/")
	string_list.insert(6, "/")
	string_list.insert(3, "/")
	new_policy_number = "".join(string_list)
	logger.info(f"Updating policy_number {policy_number} to {new_policy_number}")
	# TODO Update metadata in DB. by metadata_id=2 & document_id
	return new_policy_number

def request_raise_exception(result, message):
	try:
		result.raise_for_status()
	except Exception as ex:
		print_a_log(ex)
		return message

def add_to_cabinet(document_id, client_id):
	# Removing slashes from policy_number
	# policy_number = result = re.sub('[^0-9]','', policy_number)
	result = mayan_database.get_cabinet_by_label(client_id)

	if not result:
		result = requests.post(f"http://{mayan_app_host}/api/cabinets/",
		data={
			"documents_pk_list": f"{document_id}",
			"label": client_id,
			"parent": CLIENTS_CABINET_ID
		}, auth=AUTH)
		print(result.json())
		request_raise_exception(
			result,
			f"{os.environ.get('MAYAN_APP_USER_NAME')} did not create cabinet with label: {client_id}. code => {result.status_code}"
		)
	else:
		cabinet_id = result.get('id')
		result = requests.get(f"http://{mayan_app_host}/api/cabinets/{cabinet_id}/documents/", auth=AUTH)
		request_raise_exception(result, f"Could not fetch cabinet {client_id}'s docs'. code => {result.status_code}")
		
		result = result.json()['results']
		documents_pk_list = ""
		for x in result:
			if len(documents_pk_list) == 0:
				documents_pk_list = str(x['id'])
			else:
				documents_pk_list = f"{documents_pk_list},{x['id']}"

		result = requests.post(f"http://{mayan_app_host}/api/cabinets/{cabinet_id}/documents/",
		data={"documents_pk_list": f"{documents_pk_list},{document_id}"}, auth=AUTH)
		request_raise_exception(result, f"Did not add doc to cabinet: {client_id}. code => {result.status_code}")

	return True

@api_view()
def index(request):
	logger.debug("Logger error")
	return Response({"endpoints": [
		"/attachclient"
	]})


@api_view(['GET', 'POST'])
def attach_client(request):

	if (request.method == 'POST'):
		# policy_number = request.data.get('policy_number')
		# if (len(policy_number) == 17):
		# 	policy_number = alter_policy_number(policy_number)
		#	#TODO Add logic to update policy no in db

		client_id = None
		if request.data.get('client_number'):
			client_id = request.data.get('client_number')
		elif False:
			# TODO query for client no in AIMs
			pass

		document_id= request.data.get('document_id')

		if not client_id:
			return Response({"message": "No client ID was found."}, 400)

		## try adding client_number metadata
		mayan_database.insert_metadata({
			'metatype_id': metatype_id.get('id'),
			'client_id': client_id,
			'document_id': document_id
		})
		
		result = add_to_cabinet(document_id, client_id)
		if not (result == True):
			return Response({"add_to_cabinet_error": result}, 400)

		return Response({"message": "Operations were successfull"})
	else:
		return Response({
			"accepts": "POST",
			"body": "policy_number & document_id"
		})

