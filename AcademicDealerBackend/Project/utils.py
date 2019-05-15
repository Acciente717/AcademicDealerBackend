from django.utils import timezone

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

class LoginFail(RuntimeError):
    pass

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
    "content_type":"project",
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
    "content_type":"project",
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

def build_project_view(action, status, id, project, members, comments):
    resp = '''\
{
    "dir":"response",
    "content_type":"project",
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
}''' % (action, status, id, project.name, project.owner.email,
        timezone.localtime(project.start_date), timezone.localtime(project.end_date), project.member_total_need,
        project.description, timezone.localtime(project.create_date), timezone.localtime(project.modified_date), members, comments)
    return resp

def build_project_list_view(action, status, projects):
    resp = '''\
{
    "dir":"response",
    "content_type":"project",
    "content":
    {
        "action":"%s",
        "data":
        {
            "status":%d,
            "projects":%s,
            "total_num":%d
        }
    }
}''' % (action, status, repr(projects[:100]), len(projects))
    return resp

def build_comment_view(action, status, id, comment):
    resp = '''\
{
    "dir":"response",
    "content_type":"project",
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
    "content_type":"project",
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
