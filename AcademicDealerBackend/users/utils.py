REGISTER_SUCCESS = 0
REGISTER_DUPLICATE_MAIL_NICKNAME = 1
REGISTER_INVALID_FIELD = 2
REGISTER_INVALID_JSON = 3
REGISTER_OTHER_ERROR = 4

def assert_dir(dic, val):
    if dic['dir'] != val:
        raise AttributeError('Invalid value in "dir"!')

def assert_content_type(dic, val):
    if dic['content_type'] != val:
        raise AttributeError('Invalud value in "content_type"!')

def assert_account_action(dic, val):
    if dic['content']['action'] != val:
        raise AttributeError('Invalud value in "content":"action"!')

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
''' % (dic['signature']['user_email'], dic['signature']['password_hash'], 0)
    return resp

def gen_register_fail(dic, errno):
    if errno != REGISTER_INVALID_JSON and errno != REGISTER_INVALID_FIELD:
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
