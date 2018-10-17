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


    def tearDown(self):
        """Runs towards the end of each test"""
        Recommendation.remove_all()

    def test_index(self):
        """ Test the index page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertIn('', resp.data)

    def test_get_recommendation(self):
        resp = self.app.get('/recommendations/2')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'iPhone')

    def test_get_nonexisting_recommendation(self):
        """ Get a nonexisting recommendation """
        resp = self.app.get('/recommendations/5')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_create_recommendation(self):
        new_recommenation = dict(id=9999, name='Table', suggestion='Chair', category='Home Appliances')
        data = json.dumps(new_recommenation)
        resp = self.app.post('/recommendations', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set

    def test_create_recommendation_no_content_type(self):
        """ Create a recommendation with no Content-Type """
        new_recommedation = {'category': 'Sports'}
        data = json.dumps(new_pet)
        resp = self.app.post('/recommendations', data=data)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    def test_call_recommendation_with_an_id(self):
        """ Call create passing an id """
        new_reco = {'name': 'Car', 'category': 'Automobile'}
        data = json.dumps(new_reco)
        resp = self.app.post('/recommendations/7', data=data)
        self.assertEqual(resp.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_all_recommendations(self):
        resp = self.app.get('/recommendations')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_update_recommendation(self):
        recommendation = Recommendation.find(2)
        new_recommedation = dict(id=2, name='iPhone', suggestion='iphone pop ups', category='Electronics')
        data = json.dumps(new_recommedation)
        resp = self.app.put('/recommendations/{}'.format(2), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['suggestion'], 'iphone pop ups')

    def test_update_recommendation_not_found(self):
        """ Update a Recommendation that doesn't exist """
        new_reco = dict(id=3, name='samsung', suggestion='samsung pop ups', category='Electronocs')
        data = json.dumps(new_reco)
        resp = self.app.put('/new_reco/3', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_query_recommendation_by_category(self):
        """ Query Recommendations by Category """
        resp = self.app.get('/recommendations', query_string='category=Comics')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn('Infinity Gauntlet', resp.data)
        self.assertNotIn('iPhone', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['category'], 'Comics')

    



    def test_delete_recommendation(self):
        # save the current number of pets for later comparrison
        recommendation_count = self.get_recommendation_count()
        # delete a pet
        resp = self.app.delete('/recommendations/2', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_recommendation_count()
        self.assertEqual(new_count, recommendation_count - 1)

######################################################################
# Utility functions
######################################################################

    def get_recommendation_count(self):
        """ save the current number of recommendations """
        resp = self.app.get('/recommendations')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)

 ######################################################################
 #   M A I N
 ######################################################################
if __name__ == '__main__':
    unittest.main()
