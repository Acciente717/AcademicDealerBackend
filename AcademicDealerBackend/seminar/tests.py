from django.test import TestCase
from django.test import TransactionTestCase
from django.urls import reverse
import os, re, json, traceback

# Create your tests here.

class SeminarTestsAgent(TransactionTestCase):
    def relay(self, reverse_value, content):
        return self.client.post(
            reverse(reverse_value),
            content,
            content_type='application/json').content.decode('utf-8')

# test core functions mentioned in ../../manual_test
# in progress
class CoreFunctionalTest(TransactionTestCase):
    def get_resp(self):
        input_dir = "/home/tp/AcademicDealerBackend/manual_test/json_inputs/"
        filelist = sorted(list(os.walk(input_dir))[0][2])
        ignorelist = ["2comment_create.json"]
        for file in filelist:
            try:
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
                    json_str_out = self.client.post(
                        reverse(target + ':' + op), json_in,
                        content_type='application/json').content.decode('utf-8')
                    print("\n ##### output ####\n")
                    print(json_str_out)
                    with open("/home/tp/AcademicDealerBackend/manual_test/json_outputs/resp_" +
                              file, "w") as outfile:
                        outfile.write(json_str_out)
            except Exception as e:
                print("Exception at " + file + ' -> ' + str(finding))
                print(traceback.format_exc())
                # time.sleep(1)
        pass

    def test_core_functions(self):
        self.get_resp()
        pass
