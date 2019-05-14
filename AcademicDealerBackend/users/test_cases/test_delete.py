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

# references
