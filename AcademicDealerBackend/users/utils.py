# register status code
# 0 -- success
# 1 -- email or nickname already registered
# 2 -- invalid field (like date must be in "yyyy-mm-dd")
# 3 -- corrupted JSON
# 4 -- missing JSON field
# 5 -- bad req/resp or content_type etc. in JSON
# 6 -- other failure
REGISTER_SUCCESS = 0
REGISTER_DUPLICATE_MAIL_NICKNAME = 1
REGISTER_INVALID_FIELD = 2
REGISTER_CORRUPTED_JSON = 3
REGISTER_MISSING_FIELD = 4
REGISTER_BAD_TYPE = 5
REGISTER_OTHER_ERROR = 6

# login status code
# 0 -- success
# 1 -- wrong password
# 2 -- account not found
# 3 -- missing JSON field
# 4 -- corrupted JSON
# 5 -- bad req/resp or content_type etc. in JSON
# 6 -- other failure
LOGIN_SUCCESS = 0
LOGIN_WRONG_PASSWORD = 1
LOGIN_EMAIL_NOT_FOUND = 2
LOGIN_MISSING_FIELD = 3
LOGIN_CORRUPTED_JSON = 4
LOGIN_BAD_TYPE = 5
LOGIN_OTHER_ERROR = 6

# view status code
# 0 -- success
# 1 -- wrong password
# 2 -- account not found
# 3 -- missing JSON field
# 4 -- corrupted JSON
# 5 -- bad req/resp or content_type etc. in JSON
# 6 -- other failure
VIEW_SUCCESS = 0
VIEW_WRONG_PASSWORD = 1
VIEW_EMAIL_NOT_FOUND = 2
VIEW_MISSING_FIELD = 3
VIEW_CORRUPTED_JSON = 4
VIEW_BAD_TYPE = 5
VIEW_OTHER_ERROR = 6

# edit status code
# 0 -- success
# 1 -- wrong password
# 2 -- account not found
# 3 -- duplicated nickname
# 4 -- missing JSON field
# 5 -- corrupted JSON
# 6 -- bad req/resp or content_type etc. in JSON
# 7 -- other failure
EDIT_SUCCESS = 0
EDIT_WRONG_PASSWORD = 1
EDIT_EMAIL_NOT_FOUND = 2
EDIT_DUPLICATED_NICKNAME = 3
EDIT_MISSING_FIELD = 4
EDIT_CORRUPTED_JSON = 5
EDIT_BAD_TYPE = 6
EDIT_OTHER_ERROR = 7

# delete status code
# 0 -- success
# 1 -- wrong password
# 2 -- account not found
# 3 -- missing JSON field
# 4 -- corrupted JSON
# 5 -- bad req/resp or content_type etc. in JSON
# 6 -- other failure
DELETE_SUCCESS = 0
DELETE_WRONG_PASSWORD = 1
DELETE_EMAIL_NOT_FOUND = 2
DELETE_MISSING_FIELD = 3
DELETE_CORRUPTED_JSON = 4
DELETE_BAD_TYPE = 5
DELETE_OTHER_ERROR = 6

class BadPassword(RuntimeError):
    pass

class BadJSONType(RuntimeError):
    pass

def assert_dir(dic, val):
    if dic['dir'] != val:
        raise BadJSONType('Invalid value in "dir"!')

def assert_content_type(dic, val):
    if dic['content_type'] != val:
        raise BadJSONType('Invalud value in "content_type"!')

def assert_account_action(dic, val):
    if dic['content']['action'] != val:
        raise BadJSONType('Invalud value in "content":"action"!')

def gen_register_success(dic):
    resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":true,
            "user_email":"%s",
            "password_hash":"%s"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (dic['signature']['user_email'], dic['signature']['password_hash'], REGISTER_SUCCESS)
    return resp

def gen_register_fail(dic, errno):
    if errno != REGISTER_CORRUPTED_JSON and errno != REGISTER_INVALID_FIELD\
        and errno != REGISTER_MISSING_FIELD and errno != REGISTER_BAD_TYPE\
        and errno != LOGIN_OTHER_ERROR:
        resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":true,
            "user_email":"%s",
            "password_hash":"%s"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (dic['signature']['user_email'], dic['signature']['password_hash'], errno)
    else:
        resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":false
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (errno)
    return resp

def gen_login_success(dic):
    resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":true,
            "user_email":"%s",
            "password_hash":"%s"
        },
    "content_type":"account",
    "content":
        {
            "action":"login",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (dic['signature']['user_email'], dic['signature']['password_hash'], LOGIN_SUCCESS)
    return resp

def gen_login_fail(dic, errno):
    if errno != LOGIN_CORRUPTED_JSON and errno != LOGIN_MISSING_FIELD\
        and errno != LOGIN_BAD_TYPE and LOGIN_OTHER_ERROR:
        resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":true,
            "user_email":"%s",
            "password_hash":"%s"
        },
    "content_type":"account",
    "content":
        {
            "action":"login",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (dic['signature']['user_email'], dic['signature']['password_hash'], errno)
    else:
        resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":false
        },
    "content_type":"account",
    "content":
        {
            "action":"login",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (errno)
    return resp

def build_user_bio_json(user, labs, projects_create, projects_attend,
                        seminars_create, seminars_attend, comments):
    resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":true,
            "user_email":"%s",
            "password_hash":"%s"
        },
    "content_type":"account",
    "content":
        {
            "action":"view",
            "data":
                {
                    "status":%s,
                    "bio":
                        {
                            "real_name":"%s",
                            "nick_name":"%s",
                            "pic_url":"%s",
                            "school":"%s",
                            "department":"%s",
                            "title":"%s",
                            "enrollment_date":"%s",
                            "labs":%s,
                            "projects_create":%s,
                            "projects_attend":%s,
                            "seminars_create":%s,
                            "seminars_attend":%s,
                            "comments":%s,
                            "profile":"%s"
                        }
                }
        }
}''' % (user.email, user.pw_hash, VIEW_SUCCESS, user.real_name,
        user.nick_name, user.pic_url, user.school, user.department,
        user.title, user.enrollment_date, repr(labs),
        repr(projects_create), repr(projects_attend),
        repr(seminars_create), repr(seminars_attend),
        repr(comments), user.profile)
    return resp

def gen_view_fail(dic, errno):
    if errno != VIEW_CORRUPTED_JSON and errno != VIEW_MISSING_FIELD\
        and errno != VIEW_BAD_TYPE and VIEW_OTHER_ERROR:
        resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":true,
            "user_email":"%s",
            "password_hash":"%s"
        },
    "content_type":"account",
    "content":
        {
            "action":"view",
            "data":
                {
                    "status":%s,
                    "bio":{}
                }
        }
}
''' % (dic['signature']['user_email'], dic['signature']['password_hash'], errno)
    else:
        resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":false
        },
    "content_type":"account",
    "content":
        {
            "action":"view",
            "data":
                {
                    "status":%s,
                    "bio"{}
                }
        }
}
''' % (errno)
    return resp

def gen_edit_success(dic):
    resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":true,
            "user_email":"%s",
            "password_hash":"%s"
        },
    "content_type":"account",
    "content":
        {
            "action":"edit",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (dic['signature']['user_email'], dic['signature']['password_hash'], EDIT_SUCCESS)
    return resp

def gen_edit_fail(dic, errno):
    if errno != EDIT_CORRUPTED_JSON and errno != EDIT_MISSING_FIELD\
        and errno != EDIT_BAD_TYPE and EDIT_OTHER_ERROR:
        resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":true,
            "user_email":"%s",
            "password_hash":"%s"
        },
    "content_type":"account",
    "content":
        {
            "action":"edit",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (dic['signature']['user_email'], dic['signature']['password_hash'], errno)
    else:
        resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":false
        },
    "content_type":"account",
    "content":
        {
            "action":"edit",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (errno)
    return resp

def gen_delete_success(dic):
    resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":true,
            "user_email":"%s",
            "password_hash":"%s"
        },
    "content_type":"account",
    "content":
        {
            "action":"delete",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (dic['signature']['user_email'], dic['signature']['password_hash'], DELETE_SUCCESS)
    return resp

def gen_delete_fail(dic, errno):
    if errno != DELETE_CORRUPTED_JSON and errno != DELETE_MISSING_FIELD\
        and errno != DELETE_BAD_TYPE and DELETE_OTHER_ERROR:
        resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":true,
            "user_email":"%s",
            "password_hash":"%s"
        },
    "content_type":"account",
    "content":
        {
            "action":"delete",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (dic['signature']['user_email'], dic['signature']['password_hash'], errno)
    else:
        resp = '''\
{
    "dir":"response",
    "signature":
        {
            "is_user":false
        },
    "content_type":"account",
    "content":
        {
            "action":"delete",
            "data":
                {
                    "status":%s
                }
        }
}
''' % (errno)
    return resp
