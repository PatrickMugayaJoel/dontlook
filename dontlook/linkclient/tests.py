# from django.test import TestCase
import mock
import os
import json
import requests
import unittest
from . import views

if os.environ.get("MAYAN_DATABASE_DB") != "test":
    exit(2)

# def mock_mdb_get_cabinet_by_label_true(**kargs):
#     return {"id":1}

# def mock_mdb_get_cabinet_by_label_false(**kargs):
#     return False

# def mock_session_get(**kwargs):
#     return {'results':[]}

# def mock_session_post(**kwargs):
#     return {}

# def mock_request_raise_exception(**kwargs):
#    return{}

class TestViews(unittest.TestCase):

    def setUp(self):
        self.post_data = {
            "document_id": 2,
            "policy_number": '1'
        }
        views.mayan_database.clear_test_tables(views.metatype_id.get('id'), self.post_data["document_id"])

    def tearDown(self):
        del self.post_data
        views.mayan_database.clear_test_tables(views.metatype_id.get('id'), self.post_data["document_id"])

    def test_alter_policy_number(self):
        self.assertEqual(views.alter_policy_number('01003010001102020'), '010/030/1/000110/2020')

    def test_attach_client(self):

        db_result = views.mayan_database.check_added_metadata(views.metatype_id.get('id'), self.post_data["document_id"])
        self.assertEqual(db_result, [])

        res = requests.post("http://localhost:8080/attachclient", data=self.post_data)
        views.request_raise_exception(res, "Requests killed the unittest: test_attach_client")

        db_result = views.mayan_database.check_added_metadata(views.metatype_id.get('id'), self.post_data["document_id"])
        self.assertEqual(len(db_result), 1)

    # @mock.patch('views.mayan_database.get_cabinet_by_label', side_effect=mock_mdb_get_cabinet_by_label_true)
    # @mock.patch('views.session.post', side_effect=mock_session_post)
    # @mock.patch('views.session.get', side_effect=mock_session_get)
    # @mock.patch('views.request_raise_exception', side_effect=mock_request_raise_exception)
    # def test_add_to_cabinet(self):
    #     views.add_to_cabinet(1, "0023")
    #     assert self.a != 2

    # def test_attach_clientl(self):
    #     "This test should fail"
    #     assert self.a == 2
    #test posting with parcel data
