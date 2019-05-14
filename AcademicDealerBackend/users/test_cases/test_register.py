__user_register_req_normal0 = {
    "dir":"request",
    "signature":
        {
            "is_user":True,
            "user_email":"normal0@test.com",
            "password_hash":"3333"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "real_name":"Donald Trump",
                    "nick_name":"tomato",
                    "pic_url":"",
                    "school":"Paradize",
                    "department":"White House",
                    "title":"Other",
                    "enrollment_date":"2000-01-01",
                    "labs":[],
                    "projects_create":[],
                    "projects_attend":[],
                    "seminars_create":[],
                    "seminars_attend":[],
                    "comments":[],
                    "profile":"#### Profile title\nProfile content\n"
                }
        }
}

__user_register_req_normal1 = {
    "dir":"request",
    "signature":
        {
            "is_user":True,
            "user_email":"normal1@test.com",
            "password_hash":"22222"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "real_name":"Donald Trump",
                    "nick_name":"potato",
                    "pic_url":"",
                    "school":"Paradize",
                    "department":"White House",
                    "title":"Other",
                    "enrollment_date":"2000-01-01",
                    "labs":[],
                    "projects_create":[],
                    "projects_attend":[],
                    "seminars_create":[],
                    "seminars_attend":[],
                    "comments":[],
                    "profile":"#### Profile title\nProfile content\n"
                }
        }
}

__user_register_req_duplicate_email = {
    "dir":"request",
    "signature":
        {
            "is_user":True,
            "user_email":"normal0@test.com",
            "password_hash":"3333"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "real_name":"Donald Trump",
                    "nick_name":"banana",
                    "pic_url":"",
                    "school":"Paradize",
                    "department":"White House",
                    "title":"Other",
                    "enrollment_date":"2000-01-01",
                    "labs":[],
                    "projects_create":[],
                    "projects_attend":[],
                    "seminars_create":[],
                    "seminars_attend":[],
                    "comments":[],
                    "profile":"#### Profile title\nProfile content\n"
                }
        }
}

__user_register_req_duplicate_nickname = {
    "dir":"request",
    "signature":
        {
            "is_user":True,
            "user_email":"nickname@test.com",
            "password_hash":"3333"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "real_name":"Donald Trump",
                    "nick_name":"tomato",
                    "pic_url":"",
                    "school":"Paradize",
                    "department":"White House",
                    "title":"Other",
                    "enrollment_date":"2000-01-01",
                    "labs":[],
                    "projects_create":[],
                    "projects_attend":[],
                    "seminars_create":[],
                    "seminars_attend":[],
                    "comments":[],
                    "profile":"#### Profile title\nProfile content\n"
                }
        }
}

__user_register_req_invalid_date = {
    "dir":"request",
    "signature":
        {
            "is_user":True,
            "user_email":"invalid@test.com",
            "password_hash":"3333"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "real_name":"Invalider",
                    "nick_name":"invalid",
                    "pic_url":"",
                    "school":"Invalid",
                    "department":"Invalid Department",
                    "title":"Other",
                    "enrollment_date":"01-01",
                    "labs":[],
                    "projects_create":[],
                    "projects_attend":[],
                    "seminars_create":[],
                    "seminars_attend":[],
                    "comments":[],
                    "profile":"#### Profile title\nProfile content\n"
                }
        }
}

__user_register_req_missing_field = {
    "dir":"request",
    "signature":
        {
            "is_user":True,
            "user_email":"invalid@test.com",
            "password_hash":"3333"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "real_name":"Invalider",
                    "pic_url":"",
                    "school":"Invalid",
                    "department":"Invalid Department",
                    "title":"Other",
                    "enrollment_date":"2000-01-01",
                    "labs":[],
                    "projects_create":[],
                    "projects_attend":[],
                    "seminars_create":[],
                    "seminars_attend":[],
                    "comments":[],
                    "profile":"#### Profile title\nProfile content\n"
                }
        }
}

__user_register_req_bad_req_type0 = {
    "dir":"response",
    "signature":
        {
            "is_user":True,
            "user_email":"invalid@test.com",
            "password_hash":"3333"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "real_name":"Invalider",
                    "nick_name":"invalid",
                    "pic_url":"",
                    "school":"Invalid",
                    "department":"Invalid Department",
                    "title":"Other",
                    "enrollment_date":"2000-01-01",
                    "labs":[],
                    "projects_create":[],
                    "projects_attend":[],
                    "seminars_create":[],
                    "seminars_attend":[],
                    "comments":[],
                    "profile":"#### Profile title\nProfile content\n"
                }
        }
}

__user_register_req_bad_req_type1 = {
    "dir":"response",
    "signature":
        {
            "is_user":False
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "real_name":"Invalider",
                    "nick_name":"invalid",
                    "pic_url":"",
                    "school":"Invalid",
                    "department":"Invalid Department",
                    "title":"Other",
                    "enrollment_date":"2000-01-01",
                    "labs":[],
                    "projects_create":[],
                    "projects_attend":[],
                    "seminars_create":[],
                    "seminars_attend":[],
                    "comments":[],
                    "profile":"#### Profile title\nProfile content\n"
                }
        }
}

__user_register_req_bad_req_type2 = {
    "dir":"response",
    "signature":
        {
            "is_user":False
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "real_name":"Invalider",
                    "nick_name":"invalid",
                    "pic_url":"",
                    "school":"Invalid",
                    "department":"Invalid Department",
                    "title":"Other",
                    "enrollment_date":"2000-01-01",
                    "labs":[],
                    "projects_create":[],
                    "projects_attend":[],
                    "seminars_create":[],
                    "seminars_attend":[],
                    "comments":[],
                    "profile":"#### Profile title\nProfile content\n"
                }
        }
}

__user_register_resp_normal0 = {
    "dir":"response",
    "signature":
        {
            "is_user":True,
            "user_email":"normal0@test.com",
            "password_hash":"3333"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "status":0
                }
        }
}

__user_register_resp_normal1 = {
    "dir":"response",
    "signature":
        {
            "is_user":True,
            "user_email":"normal1@test.com",
            "password_hash":"22222"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "status":0
                }
        }
}

__user_register_resp_duplicate_email = {
    "dir":"response",
    "signature":
        {
            "is_user":True,
            "user_email":"normal0@test.com",
            "password_hash":"3333"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "status":1
                }
        }
}

__user_register_resp_duplicate_nickname = {
    "dir":"response",
    "signature":
        {
            "is_user":True,
            "user_email":"nickname@test.com",
            "password_hash":"3333"
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "status":1
                }
        }
}

__user_register_resp_invalid_date = {
    "dir":"response",
    "signature":
        {
            "is_user":False
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "status":2
                }
        }
}

__user_register_resp_missing_field = {
    "dir":"response",
    "signature":
        {
            "is_user":False
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "status":4
                }
        }
}

__user_register_resp_bad_req_type_any = {
    "dir":"response",
    "signature":
        {
            "is_user":False
        },
    "content_type":"account",
    "content":
        {
            "action":"register",
            "data":
                {
                    "status":5
                }
        }
}

user_register_req_normals = [
    __user_register_req_normal0,
    __user_register_req_normal1
]

user_register_req_duplicates = [
    __user_register_req_duplicate_email,
    __user_register_req_duplicate_nickname
]

user_register_req_invalids = [
    __user_register_req_invalid_date
]

user_register_req_missing_fields = [
    __user_register_req_missing_field
]

user_register_req_bad_req_types = [
    __user_register_req_bad_req_type0,
    __user_register_req_bad_req_type1,
    __user_register_req_bad_req_type2
]

user_register_resp_normals = [
    __user_register_resp_normal0,
    __user_register_resp_normal1
]

user_register_resp_duplicates = [
    __user_register_resp_duplicate_email,
    __user_register_resp_duplicate_nickname
]

user_register_resp_invalids = [
    __user_register_resp_invalid_date
]

user_register_resp_missing_fields = [
    __user_register_resp_missing_field
]

user_register_resp_bad_req_types = [
    __user_register_resp_bad_req_type_any,
    __user_register_resp_bad_req_type_any,
    __user_register_resp_bad_req_type_any
]
