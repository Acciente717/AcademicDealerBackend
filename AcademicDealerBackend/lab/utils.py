from django.utils import timezone
import json

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
    response_msg = {
    "dir":"response",
    "content_type":"lab",
    "content":
    {
        "action":action,
        "data":
        {
            "status":status
        }
    }
}
    return json.dumps(response_msg)

def gen_success_response(action, status, id):
    response_msg = {
    "dir":"response",
    "content_type":"lab",
    "content":
    {
        "action":action,
        "data":
        {
            "status":status,
            "id":id
        }
    }
}
    return json.dumps(response_msg)

def gen_success_response_comment(action, status, id):
    response_msg = {
    "dir":"response",
    "content_type":"lab",
    "content":
    {
        "action":action,
        "data":
        {
            "status":status,
            "comment_id":id
        }
    }
}
    return json.dumps(response_msg)

def build_lab_view(action, status, id, lab, comments):
    resp = {
    "dir":"response",
    "content_type":"lab",
    "content":
    {
        "action":action,
        "data":
        {
            "status":status,
            "id":id,
            "name":lab.name,
            "school":lab.school,
            "department":lab.department,
            "owner":lab.owner.email,
            "address":lab.address,
            "phone":lab.phone,
            "front_page_url":lab.front_page_url,
            "pic_url":lab.pic_url,
            "logo_url":lab.logo_url,
            "supervisors":lab.supervisors,
            "description":lab.description,
            "create_date":str(timezone.localtime(lab.create_date)),
            "modified_date":str(timezone.localtime(lab.modified_date)),
            "comments":comments
        }
    }
}
    return json.dumps(resp)

def build_lab_list_view(action, status, labs):
    resp = {
    "dir":"response",
    "content_type":"lab",
    "content":
    {
        "action":action,
        "data":
        {
            "status":status,
            "labs":labs[:100],
            "total_num":len(labs)
        }
    }
}
    return json.dumps(resp)

def build_comment_view(action, status, id, comment):
    resp = {
    "dir":"response",
    "content_type":"lab",
    "content":
    {
        "action":action,
        "data":
        {
            "status":status,
            "comment_id":id,
            "owner":comment.owner.email,
            "create_date":str(timezone.localtime(comment.create_date)),
            "modified_date":str(timezone.localtime(comment.modified_date)),
            "description":comment.description
        }
    }
}
    return json.dumps(resp)

def build_search_result(action, status, ids, start, len):
    resp = {
    "dir":"response",
    "content_type":"lab",
    "content":
    {
        "action":action,
        "data":
        {
            "status":status,
            "ids":ids[start:start + len],
            "total_num":len(ids)
        }
    }
}
    return json.dumps(resp)
