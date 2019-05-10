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