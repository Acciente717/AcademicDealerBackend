__user_reset_password_req_normal = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "user_email": "login@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "reset_password",
            "data": {}
        }
}

user_reset_password_req_normals = [
    __user_reset_password_req_normal
]

__user_reset_password_resp_normal = {
    "dir": "response",
    "signature":
        {
            "is_user": True,
            "user_email": "login@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "reset_password",
            "data":
                {
                    "status": 0
                }
        }
}

user_reset_password_resp_normals = [
    __user_reset_password_resp_normal
]

# references


__user_login_create_user = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "user_email": "login@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "register",
            "data":
                {
                    "real_name": "Donald Trump",
                    "nick_name": "tomato",
                    "pic_url": "",
                    "school": "Paradize",
                    "department": "White House",
                    "title": "Other",
                    "enrollment_date": "2000-01-01",
                    "labs": [],
                    "projects_create": [],
                    "projects_attend": [],
                    "seminars_create": [],
                    "seminars_attend": [],
                    "comments": [],
                    "profile": "#### Profile title\nProfile content\n"
                }
        }
}

__user_login_req_no_user = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "user_email": "login2@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "login",
            "data": {}
        }
}

__user_login_req_wrong_password = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "user_email": "login@test.com",
            "password_hash": "2222"
        },
    "content_type": "account",
    "content":
        {
            "action": "login",
            "data": {}
        }
}

__user_login_req_missing_field = {
    "dir": "request",
    "signature":
        {
            "is_user": True,
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "login",
            "data": {}
        }
}

__user_login_req_bad_type = {
    "dir": "response",
    "signature":
        {
            "is_user": True,
            "user_email": "login@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "login",
            "data": {}
        }
}

__user_login_resp_no_user = {
    "dir": "response",
    "signature":
        {
            "is_user": True,
            "user_email": "login2@test.com",
            "password_hash": "3333"
        },
    "content_type": "account",
    "content":
        {
            "action": "login",
            "data":
                {
                    "status": 2
                }
        }
}

__user_login_resp_wrong_password = {
    "dir": "response",
    "signature":
        {
            "is_user": True,
            "user_email": "login@test.com",
            "password_hash": "2222"
        },
    "content_type": "account",
    "content":
        {
            "action": "login",
            "data":
                {
                    "status": 1
                }
        }
}

__user_login_resp_missing_field = {
    "dir": "response",
    "signature":
        {
            "is_user": False
        },
    "content_type": "account",
    "content":
        {
            "action": "login",
            "data":
                {
                    "status": 3
                }
        }
}

__user_login_resp_bad_type = {
    "dir": "response",
    "signature":
        {
            "is_user": False
        },
    "content_type": "account",
    "content":
        {
            "action": "login",
            "data":
                {
                    "status": 5
                }
        }
}

user_login_create_users = [
    __user_login_create_user
]

user_login_req_no_users = [
    __user_login_req_no_user
]

user_login_req_wrong_passwords = [
    __user_login_req_wrong_password
]

user_login_req_bad_types = [
    __user_login_req_bad_type
]

user_login_req_missing_fields = [
    __user_login_req_missing_field
]

user_login_resp_no_users = [
    __user_login_resp_no_user
]

user_login_resp_wrong_passwords = [
    __user_login_resp_wrong_password
]

user_login_resp_bad_types = [
    __user_login_resp_bad_type
]

user_login_resp_missing_fields = [
    __user_login_resp_missing_field
]
