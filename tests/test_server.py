"""
Pet API Service Test Suite
Test cases can be run with the following:
nosetests
"""

import unittest
import logging
import json
import os
from mock import MagicMock, patch
from flask_api import status    # HTTP Status Codes
from models import Recommendation, DataValidationError
import server

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409

######################################################################
#  T E S T   C A S E S
######################################################################
class TestRecommendationServer(unittest.TestCase):
    """ Recommendation Service tests """

    def setUp(self):
        """Runs before each test"""
        self.app = server.app.test_client()
        Recommendation(id=1, name='Infinity Gauntlet', suggestion='Soul Stone', category='Comics').save()
        Recommendation(id=2, name='iPhone', suggestion='iphone Case', category='Electronics').save()

    def tearDown(self):
        """Runs towards the end of each test"""
        Recommendation.remove_all()

    def test_get_recommendation(self):
        resp = self.app.get('/recommendations/2')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'iPhone')

    def test_create_recommendation(self):
        """ Create a new recommendation """
        new_recommenation = dict(id=9999, name='Table', suggestion='Chair', category='Home Appliances')
        data = json.dumps(new_recommenation)
        resp = self.app.post('/recommendations', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        # Make sure location header is set
    #location = resp.headers.get('Location', None)
    #self.assertTrue(location != None)
    # Check the data is correct
    #new_json = json.loads(resp.data)
    #self.assertEqual(new_json['name'], 'Table')

    def test_list_all_recommendations(self):
        resp = self.app.get('/recommendations')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_query_recommendation_list_by_category(self):
        resp = self.app.get('/recommendations', query_string='category=Comics')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('Infinity Gauntlet' in resp.data)
        self.assertFalse('iPhone' in resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['category'], 'Comics')
