from django.utils import timezone

# labinfo status code
# 0 -- success
# 1 -- other failure
# 2 -- no seminar
# 3 -- seminar outdated
# 4 -- permission deny
# 5 -- user login fail
# 6 -- seminar quota is full 
# 7 -- user not in the seminar
# 8 -- json corrupt
# 9 -- seminar id error
# 10 -- user already in the seminar
# 11 -- owner cannot join its own seminar
# 12 -- comment id error

STATUS_SUCCESS = 0
STATUS_OTHER_FAILURE = 1
STATUS_NO_SEMINAR = 2
STATUS_OUTDATED = 3
STATUS_PERMISSION_DENY = 4
STATUS_LOGIN_FAIL = 5
STATUS_ALREADY_FULL = 6
STATUS_NOT_IN = 7
STATUS_CORRUPTED_JSON = 8
STATUS_PROJECT_ID_ERROR = 9
STATUS_ALREADY_IN = 10
STATUS_IS_OWNER = 11
STATUS_COMMENT_ID_ERROR = 12

class LoginFail(RuntimeError):
    pass

class BadJSONType(RuntimeError):
    pass

class PermissionDenied(RuntimeError):
    pass

class SeminarIDError(RuntimeError):
    pass

class SeminarOutdated(RuntimeError):
    pass

class UserAlreadyIn(RuntimeError):
    pass

class SeminarAlreadyFull(RuntimeError):
    pass

class UserNotIn(RuntimeError):
    pass

class UserIsOwner(RuntimeError):
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

def gen_success_response_comment(action, status, id):
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
            "comment_id":%d
        }
    }
}
''' % (action, status, id)
    return response_msg

def build_seminar_view(action, status, id, seminar, members, comments):
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
            "member_total_need":%d,
            "description":"%s",
            "create_date":"%s",
            "modified_date":"%s",
            "current_members":%s
            "comments":%s
        }
    }
}''' % (action, status, id, seminar.name, seminar.owner.email,
        timezone.localtime(seminar.start_date), timezone.localtime(seminar.end_date), seminar.member_total_need,
        seminar.description, timezone.localtime(seminar.create_date), timezone.localtime(seminar.modified_date),
        members, comments)
    return resp

def build_seminar_list_view(action, status, seminars):
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
            "seminars":%s,
            "total_num":%d
        }
    }
}''' % (action, status, repr(seminars[:100]), len(seminars))
    return resp

def build_comment_view(action, status, id, comment):
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
            "comment_id":%d,
            "owner":"%s",
            "create_date":"%s",
            "modified_date":"%s",
            "description":"%s"
        }
    }
}''' % (action, status, id, comment.owner.email,
        timezone.localtime(comment.create_date), timezone.localtime(comment.modified_date), comment.description)
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
