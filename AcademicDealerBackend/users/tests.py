import json
import os
import sys
import traceback
import re
import time
# from ..seminar.tests import SeminarTestsAgent

from django.test import TransactionTestCase
from django.urls import reverse

from .test_cases.test_register import *
from .test_cases.test_login import *
from .test_cases.test_reset_password import *
from .test_cases.test_delete import *
from .test_cases.test_edit import *

from django.test import Client


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
            self.assertDictEqual(expected_resp,
                                 json.loads(resp.content.decode('utf-8')))

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
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

        for req, expected_resp in \
                zip(user_register_req_duplicates, user_register_resp_duplicates):
            resp = self.client.post(reverse('users:register'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

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
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

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
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

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
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))


class UsersLoginTests(TransactionTestCase):

    def test_login_normals(self):
        '''
        Normal login. Should be successful.
        '''

        for req in user_login_create_users:
            resp = self.client.post(reverse('users:register'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(0, json.loads(resp.content.decode('utf-8'))['content']['data']['status'])

        for req, expected_resp in \
                zip(user_login_req_normals, user_login_resp_normals):
            resp = self.client.post(reverse('users:login'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    def test_login_wrong_password(self):
        '''
        Wrong password. Should return status code 1.
        '''

        for req in user_login_create_users:
            resp = self.client.post(reverse('users:register'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(0, json.loads(resp.content.decode('utf-8'))['content']['data']['status'])

        for req, expected_resp in \
                zip(user_login_req_wrong_passwords, user_login_resp_wrong_passwords):
            resp = self.client.post(reverse('users:login'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    def test_login_no_user(self):
        '''
        Email not found. Should return status code 2.
        '''

        for req in user_login_create_users:
            resp = self.client.post(reverse('users:register'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(0, json.loads(resp.content.decode('utf-8'))['content']['data']['status'])

        for req, expected_resp in \
                zip(user_login_req_no_users, user_login_resp_no_users):
            resp = self.client.post(reverse('users:login'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    def test_login_missing_field(self):
        '''
        Missing field in JSON. Should return status code 3.
        '''

        for req in user_login_create_users:
            resp = self.client.post(reverse('users:register'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(0, json.loads(resp.content.decode('utf-8'))['content']['data']['status'])

        for req, expected_resp in \
                zip(user_login_req_missing_fields, user_login_resp_missing_fields):
            resp = self.client.post(reverse('users:login'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    def test_login_bad_types(self):
        '''
        Bad request type in JSON. Should return status code 5.
        '''

        for req in user_login_create_users:
            resp = self.client.post(reverse('users:register'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(0, json.loads(resp.content.decode('utf-8'))['content']['data']['status'])

        for req, expected_resp in \
                zip(user_login_req_bad_types, user_login_resp_bad_types):
            resp = self.client.post(reverse('users:login'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))


# class UserResetPasswordTests(TransactionTestCase):
#     def test_reset_password_normals(self):
#         '''
#         Normal reset password. Should be successful.
#         '''
#
#         for req, expected_resp in \
#                 zip(user_reset_password_req_normals, user_reset_password_resp_normals):
#             resp = self.client.post(reverse('users:reset_password'), req,
#                                     content_type='application/json')
#             self.assertEqual(resp.status_code, 200)
#             self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

class UserDeleteTests(TransactionTestCase):
    def create_user(self):
        for req, expected_resp in \
                zip(user_register_req_normals, user_register_resp_normals):
            resp = self.client.post(reverse('users:register'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    def test_normals(self):

        # Normal. Should be successful.

        self.create_user()

        for req, expected_resp in \
                zip(user_delete_req_normals, user_delete_resp_normals):
            resp = self.client.post(reverse('users:delete'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    def test_wrong_passwords(self):

        for req, expected_resp in \
                zip(user_register_req_normals, user_register_resp_normals):
            resp = self.client.post(reverse('users:register'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

        for req, expected_resp in \
                zip(user_delete_req_wrong_passwords, user_delete_resp_wrong_passwords):
            resp = self.client.post(reverse('users:delete'), req,
                                    content_type='application/json')
            # print(resp.content.decode('utf-8'))
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    def test_nonexists(self):

        for req, expected_resp in \
                zip(user_delete_req_nonexists, user_delete_resp_nonexists):
            resp = self.client.post(reverse('users:delete'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    # TODO: bugs in views.py:delete require fixing:
    # TODO: when fields are not used, missing cannot be detected
    # def test_missing_json_fields(self):
    #     self.create_user()
    #     for req, expected_resp in \
    #             zip(user_delete_req_missing_json_fields, user_delete_resp_missing_json_fields):
    #         resp = self.client.post(reverse('users:delete'), req,
    #                                 content_type='application/json')
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    # TODO
    # def test_missing_corrupted_jsons(self):
    #     self.create_user()
    #     for req, expected_resp in \
    #             zip(user_delete_req_normals, user_delete_resp_missing_json_fields):
    #         resp = self.client.post(reverse('users:delete'), corrupt(req),
    #                                 content_type='application/json')
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    # TODO: flaw in json format specification
    def test_bad_reqs(self):
        self.create_user()
        for req, expected_resp in \
                zip(user_delete_req_bad_reqs, user_delete_resp_bad_reqs):
            resp = self.client.post(reverse('users:delete'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            out = json.loads(resp.content.decode('utf-8'))
            # print(out)
            self.assertDictEqual(expected_resp, out)


class UserEditTests(TransactionTestCase):
    def create_user(self):
        for req, expected_resp in \
                zip(user_register_req_normals, user_register_resp_normals):
            resp = self.client.post(reverse('users:register'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    def test_normals(self):

        self.create_user()

        for req, expected_resp in \
                zip(user_edit_req_normals, user_edit_resp_normals):
            resp = self.client.post(reverse('users:edit'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    def test_non_exists(self):

        # self.create_user()

        for req, expected_resp in \
                zip(user_edit_req_normals, user_edit_resp_non_exists):
            resp = self.client.post(reverse('users:edit'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    def test_wrong_password(self):

        self.create_user()

        for req, expected_resp in \
                zip(user_edit_req_wrong_passwords, user_edit_resp_wrong_passwords):
            resp = self.client.post(reverse('users:edit'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    # TODO: Bugs in user.edit require fixing:
    # TODO: missing edit.data field is not properly handled
    def test_missing_json_fields(self):
        self.create_user()
        for req, expected_resp in \
                zip(user_edit_req_missing_json_fields, user_edit_resp_missing_json_fields):
            resp = self.client.post(reverse('users:edit'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            out = json.loads(resp.content.decode('utf-8'))
            # print(out)
            self.assertDictEqual(expected_resp, out)

    # def test_missing_corrupted_jsons(self):
    #     self.create_user()
    #     for req, expected_resp in \
    #             zip(user_edit_req_normals, user_edit_resp_missing_json_fields):
    #         resp = self.client.post(reverse('users:edit'), corrupt(req),
    #                                 content_type='application/json')
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertDictEqual(expected_resp, json.loads(resp.content.decode('utf-8')))

    # TODO: flaw in json format specification
    # TODO: same as user.delete
    def test_bad_reqs(self):
        self.create_user()
        for req, expected_resp in \
                zip(user_edit_req_bad_reqs, user_edit_resp_bad_reqs):
            resp = self.client.post(reverse('users:edit'), req,
                                    content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            out = json.loads(resp.content.decode('utf-8'))
            # print(out)
            self.assertDictEqual(expected_resp, out)


# absolute path accomandated to local tests
input_dir = "/home/tp/AcademicDealerBackend/manual_test/json_inputs/"
output_dir = "/home/tp/AcademicDealerBackend/manual_test/json_outputs/resp_"


# test core functions mentioned in ../../manual_test
# in progress
class CoreFunctionalTest(TransactionTestCase):
    def get_resp(self):
        try:
            file = finding = "F"
            filelist = sorted(list(os.walk("input_dir"))[0][2])
            ignorelist = ["2comment_create.json"]
            for file in filelist:

                if file in ignorelist:
                    continue
                print("dealing with " + file)
                finding = re.findall(r"\d*(.*)_(.*)\d*\..*", file)[0]
                target, op = finding

                with open(input_dir + file) as in_file:
                    json_in = json.load(in_file)
                    print("\n ##### case  #####\n")
                    print(file)
                    print("\n ##### target ####\n")
                    print(target + ':' + op)
                    print("\n ##### input #####\n")
                    print(json_in)
                    # json_str_out = Client().post(
                    #     "/%s/%s" % (target, op), json_in,
                    #     content_type='application/json').content.decode('utf-8')
                    json_str_out = self.client.post(
                        reverse(target + ':' + op), json_in,
                        content_type='application/json').content.decode('utf-8')
                    print("\n ##### output ####\n")
                    print(json_str_out)
                    with open(output_dir +
                              file, "w") as outfile:
                        outfile.write(json_str_out)
        except Exception as e:
            print("remote tests. local cases disabled")
            pass

    def test_core_functions(self):
        self.get_resp()
        pass
