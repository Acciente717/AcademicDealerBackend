from django.utils import timezone
import json

# labinfo status code
# 0 -- success
# 1 -- other failure
# 2 -- project outdated
# 3 -- permission deny
# 4 -- user login fail
# 5 -- project quota is full 
# 6 -- user not in the project
# 7 -- json corrupt
# 8 -- project id error
# 9 -- user already in the project
# 10 -- comment id error
# 11 -- owner is trying to drop out of project

STATUS_SUCCESS = 0
STATUS_OTHER_FAILURE = 1
STATUS_OUTDATED = 2
STATUS_PERMISSION_DENY = 3
STATUS_LOGIN_FAIL = 4
STATUS_ALREADY_FULL = 5
STATUS_NOT_IN = 6
STATUS_CORRUPTED_JSON = 7
STATUS_PROJECT_ID_ERROR = 8
STATUS_ALREADY_IN = 9
STATUS_COMMENT_ID_ERROR = 10
STATUS_IS_OWNER = 11

class BadJSONType(RuntimeError):
    pass

class PermissionDenied(RuntimeError):
    pass

class ProjectIDError(RuntimeError):
    pass

class CommentIDError(RuntimeError):
    pass

class ProjectOutdated(RuntimeError):
    pass

class UserAlreadyIn(RuntimeError):
    pass

class ProjectAlreadyFull(RuntimeError):
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
    response_msg = {
    "dir":"response",
    "content_type":"project",
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
    "content_type":"project",
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
    "content_type":"project",
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

def build_project_view(action, status, id, project, members, comments):
    resp = {
    "dir":"response",
    "content_type":"project",
    "content":
    {
        "action":action,
        "data":
        {
            "status":status,
            "id":id,
            "name":project.name,
            "owner":project.owner.email,
            "start_date":str(project.start_date),
            "end_date":str(project.end_date),
            "member_total_need":project.member_total_need,
            "description":project.description,
            "create_date":str(project.create_date),
            "modified_date":str(project.modified_date),
            "current_members":members,
            "comments":comments
        }
    }
}
    return json.dumps(resp)

def build_project_list_view(action, status, projects):
    resp = {
    "dir":"response",
    "content_type":"project",
    "content":
    {
        "action":action,
        "data":
        {
            "status":status,
            "projects":projects[:100],
            "total_num":len(projects)
        }
    }
}
    return json.dumps(resp)

def build_comment_view(action, status, id, comment):
    resp = {
    "dir":"response",
    "content_type":"project",
    "content":
    {
        "action":action,
        "data":
        {
            "status":status,
            "comment_id":id,
            "owner":comment.owner.email,
            "create_date":str(comment.create_date),
            "modified_date":str(comment.modified_date),
            "description":comment.description
        }
    }
}
    return json.dumps(resp)

def build_search_result(action, status, ids, start, len):
    resp = {
    "dir":"response",
    "content_type":"project",
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
