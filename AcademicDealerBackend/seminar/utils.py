# labinfo status code
# 0 -- success
# 1 -- no seminar
# 2 -- seminar outdated
# 3 -- permission deny
# 4 -- user login fail
# 5 -- seminar quota is full 
# 6 -- user not in the seminar
# 7 -- json corrupt
# 8 -- seminar id error
# 9 -- user already in the seminar
# 10 -- other failure
STATUS_SUCCESS = 0
STATUS_NO_PROJECT = 1
STATUS_OUTDATED = 2
STATUS_PERMISSION_DENY = 3
STATUS_LOGIN_FAIL = 4
STATUS_ALREADY_FULL = 5
STATUS_NOT_IN = 6
STATUS_CORRUPTED_JSON = 7
STATUS_PROJECT_ID_ERROR = 8
STATUS_ALREADY_IN = 9
STATUS_OTHER_FAILURE = 10

class LoginFail(RuntimeError):
    pass

class BadJSONType(RuntimeError):
    pass

class PERMISSION_DENY(RuntimeError):
    pass

class PROJECT_ID_ERROR(RuntimeError):
    pass

class OUTDATE(RuntimeError):
    pass

class ALREADY_IN(RuntimeError):
    pass

class ALREADY_FULL(RuntimeError):
    pass

class NOT_IN(RuntimeError):
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
    "content_type":"seminar",
    "content":
    {
        "action":"%s",
        "data":
        {
            "status":%d
        }
    }
}
''' % (action, status)
    return response_msg

def gen_success_response(action, status, id):
    response_msg = '''
{
    "dir":"response",
    "content_type":"seminar",
    "content":
    {
        "action":"%s",
        "data":
        {
            "status":%d,
            "id":%d
        }
    }
}
''' % (action, status, id)
    return response_msg

def build_seminar_view(action, status, id, seminar, members):
    resp = '''\
{
    "dir":"response",
    "content_type":"seminar",
    "content":
    {
        "action":"%s",
        "data":
        {
            "status":%d,
            "id":%d,
            "name":"%s",
            "owner":"%s",
            "start_date":"%s",
            "end_date":"%s",
            "member_number_limit":%d,
            "description":"%s",
            "current_members":%s
        }
    }
}''' % (action, status, id, seminar.name, seminar.owner.email,
        seminar.start_date, seminar.end_date, seminar.member_number_limit,
        seminar.description, members)
    return resp

def build_search_result(action, status, ids, start, end):
    resp = '''\
{
    "dir":"response",
    "content_type":"seminar",
    "content":
    {
        "action":"%s",
        "data":
        {
            "status":%s,
            "ids":%s,
            "total_num":%s
        }
    }
}''' % (action, status, repr(ids[start:end]), len(ids))
    return resp
