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

mayan_app_host = os.environ.get("MAYAN_APP_HOST")

session = requests.Session()
logger = logging.getLogger(__name__)

def print_a_log(msg):
	print(f"\nError: {msg}")
	logger.critical(f'\n\n{msg}\n\n')

start_time = time.perf_counter()
print("Connecting to mayan")
while True:
	try:
		session.headers.update(requests.post(
			f'http://{mayan_app_host}/api/auth/token/obtain/?format=json',
			data={'username': os.environ.get("MAYAN_APP_USER_NAME"), 'password': os.environ.get("MAYAN_APP_USER_PASS")}
		).json())
		break
	except Exception as ex:
		if time.perf_counter() - start_time >= 30:
			print_a_log("Auto app to Mayan Connection failed!!")
			sys.exit()
		print("Trying again in 2sec..")
		time.sleep(2)

mayan_database = MayanDatabaseConnection()


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
		result = session.post(f"http://{mayan_app_host}/api/cabinets/",
		data={
			"documents_pk_list": f"{document_id}",
			"label": client_id,
			"parent": 1
		})
		request_raise_exception(
			result,
			f"{os.environ.get('MAYAN_APP_USER_NAME')} did not create cabinet with label: {client_id}. code => {result.status_code}"
		)
	else:
		cabinet_id = result.get('id')
		result = session.get(f"http://{mayan_app_host}/api/cabinets/{cabinet_id}/documents/")
		request_raise_exception(result, f"Could not fetch cabinet {client_id}'s docs'. code => {result.status_code}")
		
		result = result.json()['results']
		documents_pk_list = ""
		for x in result:
			if len(documents_pk_list) == 0:
				documents_pk_list = str(x['id'])
			else:
				documents_pk_list = f"{documents_pk_list},{x['id']}"

		result = session.post(f"http://{mayan_app_host}/api/cabinets/{cabinet_id}/documents/",
		data={"documents_pk_list": f"{documents_pk_list},{document_id}"})
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

		# # '010/030/1/000110/2020'
		# result = mayan_database.get_doc_id_by_policy_no(policy_number) # TODO many docs could have the same policy_number
		# document_id = result.get('document_id')
		# if not document_id:
		# 	return Response({"message": "Request failed! Metadata id not found"}, 404)

		# TODO query for the client id in AIMs
		client_id = '00125'
		client_no_metatype_id = 1
		document_id=1

		print(request.data)

		result = mayan_database.insert_metadata_by_policy_no({
			'metatype_id': client_no_metatype_id,
			'client_id': client_id,
			'document_id': document_id
		})
		if not result:
			return Response({"message": "Update db query failed!"}, 400)
		
		# result = add_to_cabinet(document_id, client_id)
		# if not (result == True):
		# 	return Response({"add_to_cabinet_error": result}, 400)

		return Response({"message": "Operations were successfull"})
	else:
		return Response({
			"accepts": "POST",
			"body": "policy_number & document_id"
		})

