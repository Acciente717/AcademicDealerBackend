# labinfo status code
# 0 -- success
# 1 -- no project
# 2 -- account not found
# 3 -- missing JSON field
# 4 -- corrupted JSON
# 5 -- bad req/resp or content_type etc. in JSON
# 6 -- other failure
STATUS_SUCCESS = 0
STATUS_NO_PROJECT = 1
STATUS_OUTDATED = 2
STATUS_INVALID_ACCOUNT = 3
STATUS_LOGIN_FAIL = 4
STATUS_ALREADY_FULL = 5
STATUS_OTHER_FAILURE = 6
STATUS_CORRUPTED_JSON = 7

class LoginFail(RuntimeError):
    pass

class BadJSONType(RuntimeError):
    pass

def assert_dir(dic, val):
    if dic['dir'] != val:
        raise BadJSONType('Invalid value in "dir"!')

def assert_content_type(dic, val):
    if dic['content_type'] != val:
        raise BadJSONType('Invalud value in "content_type"!')

def assert_action(dic, val):
    if dic['content']['action'] != val:
        raise BadJSONType('Invalud value in "content":"action"!')

def gen_fail_response(action, status):
    response_msg = '''
{
    "dir":"response",
    "content_type":"project",
    "content":
    {
        "action":"%s",
        "data":
        {
            "status":%s
        }
    }
}
''' % (action, status)
    return response_msg

def gen_success_response(action, status, id):
    response_msg = '''
{
    "dir":"response",
    "content_type":"project",
    "content":
    {
        "action":"%s",
        "data":
        {
            "status":%s
            "id":%d
        }
    }
}
''' % (action, status, id)
    return response_msg