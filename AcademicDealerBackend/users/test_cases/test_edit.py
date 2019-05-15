
# change nick name
__user_edit_req_normal = {
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
            "action": "edit",
            "data": {
                    "real_name": "Donald Trump",
                    "nick_name": "potato",
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

user_edit_req_normals = [
    __user_edit_req_normal
]

__user_edit_resp_normal = {
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
            "action": "edit",
            "data":
                {
                    "status": 0
                }
        }
}

user_edit_resp_normals = [
    __user_edit_resp_normal
]

# non-exists

__user_edit_resp_non_exist = {
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
            "action": "edit",
            "data":
                {
                    "status": 2
                }
        }
}

user_edit_resp_non_exists = [
    __user_edit_resp_non_exist
]

# wrong pw

__user_edit_req_wrong_password = {
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
            "action": "edit",
            "data": {
                    "real_name": "Donald Trump",
                    "nick_name": "potato",
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

user_edit_req_wrong_passwords = [
    __user_edit_req_normal
]

__user_edit_resp_wrong_password = {
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
            "action": "edit",
            "data":
                {
                    "status": 1
                }
        }
}

user_edit_resp_wrong_passwords = [
    __user_edit_resp_wrong_password
]

# missing json field

# missing content.data
__user_edit_missing_json_field = {
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
            "action": "edit",
        }
}

user_edit_req_missing_json_fields = [
    __user_edit_missing_json_field
]

__user_edit_resp_missing_json_field = {
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
            "action": "edit",
            "data":
                {
                    "status": 4
                }
        }
}

user_edit_resp_missing_json_fields = [
    __user_edit_resp_missing_json_field
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
                    "status": 5
                }
        }
}

user_delete_resp_bad_reqs = [
    __user_delete_resp_bad_req
]
