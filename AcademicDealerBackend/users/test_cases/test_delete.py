__user_delete_req_normal = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
            "data": {}
        }
}

user_delete_req_normals = [
    __user_delete_req_normal
]

__user_delete_resp_normal = {
    "dir": "response",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
            "data":
                {
                    "status": 0
                }
        }
}

user_delete_resp_normals = [
    __user_delete_resp_normal
]

# non exists

__user_delete_req_nonexist = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
            "data": {}
        }
}

user_delete_req_nonexists = [
    __user_delete_req_nonexist
]

__user_delete_resp_nonexist = {
    "dir": "response",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
            "data":
                {
                    "status": 2
                }
        }
}

user_delete_resp_nonexists = [
    __user_delete_resp_nonexist
]

# wrong pw

__user_delete_req_wrong_password = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3332"
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
            "data": {}
        }
}

user_delete_req_wrong_passwords = [
    __user_delete_req_wrong_password
]

__user_delete_resp_wrong_password = {
    "dir": "response",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3332"
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
            "data":
                {
                    "status": 1
                }
        }
}

user_delete_resp_wrong_passwords = [
    __user_delete_resp_wrong_password
]

# missing json field

# missing content.data
__user_delete_missing_json_field = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
        }
}

user_delete_req_missing_json_fields = [
    __user_delete_missing_json_field
]

__user_delete_resp_missing_json_field = {
    "dir": "response",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
            "data":
                {
                    "status": 3
                }
        }
}

user_delete_resp_missing_json_fields = [
    __user_delete_resp_missing_json_field
]

# missing corrupted JSON
__user_delete_req_corrupted_json = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
        }
}

user_delete_req_corrupted_jsons = [
    __user_delete_req_corrupted_json
]

__user_delete_resp_corrupted_json = {
    "dir": "response",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
            "data":
                {
                    "status": 4
                }
        }
}

user_delete_resp_corrupted_jsons = [
    __user_delete_resp_corrupted_json
]

# 5: bad req
__user_delete_req_bad_req = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "user_email": "normal0@test.com",
            "password_hash": "3333"
        },
    "content_type": "bad",
    "content":
        {
            "action": "delete",
            "data": {}
        }
}

user_delete_req_bad_reqs = [
    __user_delete_req_bad_req
]

__user_delete_resp_bad_req = {
    "dir": "response",
    "signature":
        {
            "is_user": False
        },
    "content_type": "account",
    "content":
        {
            "action": "delete",
            "data":
                {
                    "status": 5
                }
        }
}

user_delete_resp_bad_reqs = [
    __user_delete_resp_bad_req
]
