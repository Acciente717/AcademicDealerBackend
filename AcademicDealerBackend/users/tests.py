from django.test import TransactionTestCase
from django.urls import reverse
from .test_utils import *
import json

class UsersRegisterTests(TransactionTestCase):

    def test_register_normals(self):
        '''
        Normal register. Should be successful.
        '''

        for req, expected_resp in \
            zip(user_register_req_normals, user_register_resp_normals):
            resp = self.client.post(reverse('users:register'), req,
                content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content))
    
    def test_register_duplicates(self):
        '''
        Duplicate register. Either duplicating email or nickname.
        Sould return status code 1.
        '''

        for req, expected_resp in \
            zip(user_register_req_normals, user_register_resp_normals):
            resp = self.client.post(reverse('users:register'), req,
                content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content))

        for req, expected_resp in \
            zip(user_register_req_duplicates, user_register_resp_duplicates):
            resp = self.client.post(reverse('users:register'), req,
                content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content))
    
    def test_register_invalids(self):
        '''
        Invalid field test. Date must be in the form of "yyyy-mm-dd".
        Should return status code 2.
        '''

        for req, expected_resp in \
            zip(user_register_req_invalids, user_register_resp_invalids):
            resp = self.client.post(reverse('users:register'), req,
                content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content))

    def test_register_missing_fields(self):
        '''
        Missing field test.
        Should return status code 4.
        '''

        for req, expected_resp in \
            zip(user_register_req_missing_fields, user_register_resp_missing_fields):
            resp = self.client.post(reverse('users:register'), req,
                content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content))
    
    def test_register_bad_request_types(self):
        '''
        Missing field test.
        Should return status code 4.
        '''

        for req, expected_resp in \
            zip(user_register_req_bad_req_types, user_register_resp_bad_req_types):
            resp = self.client.post(reverse('users:register'), req,
                content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content))
