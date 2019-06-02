import traceback

import json
import os
import sys

from django.test import TransactionTestCase
from django.urls import reverse
sys.path.append("../../AcademicDealerBackend/users/")



import sys

input_dir = "./AcademicDealerBackend/manual_test/json_inputs/"


def get_resp():
    li = list(os.walk(input_dir))[0][2]
    for file in li:
        print(file)
        try:
            with open(input_dir + file) as in_file:
                json_in = json.load(in_file)
                json_out =CoreFunctionalTest().get_resp(
                    reverse('users:register'), json_in,
                    content_type='application/json')
                with open("./AcademicDealerBackend/manual_test/json_outputs", "w") as outfile:
                    outfile.write(json_out)
        except Exception as e:
            traceback.print_exc()


if __name__ == "__main__":
    get_resp()
