from django.utils import timezone

# labinfo status code
# 0 -- success
# 1 -- other failure
# 2 -- lab outdated
# 3 -- permission deny
# 4 -- user login fail
# 5 -- lab quota is full 
# 6 -- user not in the lab
# 7 -- json corrupt
# 8 -- lab id error
# 9 -- user already in the lab
# 10 -- comment id error
# 11 -- owner is trying to drop out of lab

STATUS_SUCCESS = 0
STATUS_OTHER_FAILURE = 1
STATUS_PERMISSION_DENY = 2
STATUS_LOGIN_FAIL = 3
STATUS_CORRUPTED_JSON = 4
STATUS_LAB_ID_ERROR = 5
STATUS_COMMENT_ID_ERROR = 6

class BadJSONType(RuntimeError):
    pass

class PermissionDenied(RuntimeError):
    pass

class LabIDError(RuntimeError):
    pass

class CommentIDError(RuntimeError):
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
    "content_type":"lab",
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
    "content_type":"lab",
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
    "content_type":"lab",
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

def build_lab_view(action, status, id, lab, comments):
    resp = '''\
{
    "dir":"response",
    "content_type":"lab",
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
            "description":"%s",
            "create_date":"%s",
            "modified_date":"%s",
            "comments":%s
        }
    }
}''' % (action, status, id, lab.name, lab.owner.email,
        timezone.localtime(lab.start_date), timezone.localtime(lab.end_date),
        lab.description, timezone.localtime(lab.create_date), timezone.localtime(lab.modified_date), comments)
    return resp

def build_lab_list_view(action, status, labs):
    resp = '''\
{
    "dir":"response",
    "content_type":"lab",
    "content":
    {
        "action":"%s",
        "data":
        {
            "status":%d,
            "labs":%s,
            "total_num":%d
        }
    }
}''' % (action, status, repr(labs[:100]), len(labs))
    return resp

def build_comment_view(action, status, id, comment):
    resp = '''\
{
    "dir":"response",
    "content_type":"lab",
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

def build_search_result(action, status, ids, start, len):
    resp = '''\
{
    "dir":"response",
    "content_type":"lab",
    "content":
    {
        "action":"%s",
        "data":
        {
            "status":%s,
            "ids":%s,
            "total_num":%d
        }
    }
}''' % (action, status, repr(ids[start:start + len]), len(ids))
    return resp
