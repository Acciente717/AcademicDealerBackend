# JSON Format Specification

## Type definition rule

1. `data` is the root type.
2. The type of an object is defined as `obj0 = { field0, field1 }`. The type of its field is refered as `obj0.field0`.
3. When applying the definition of an object, the field refers to the corresponding string as the key. For example, an instance of `obj0 = { field0 = Number, field1 = Bool }` would be `{ "field0": 0, "field1": true }`.
4. The type of an array is defined as `arr0 = [ elem0 ]`. The type of its element is refered as `arr0.[elem0]`. Note that all elements of the same array should have the same type. i.e. `[1, true, "god"]` is illegal.
5. Basic types are noted with capital letter. That is one of `String`, `Number`, `Boolean`, `Array`, `Object` and `Null`. (don't actually use `Null`, it's pure evil.)
6. The enumeration values of a given type is defined like `enum0 = String ( "foo" | "bar" )`.
7. Comments begin with `--` and expand to the end of the line.
8. The definition may be recursively expanded or it can appear as a new top level definition.
9. `other` is a valid field for all objects. We use this field to implement extensions.
10. `prefix a` will add `a.` to all top level definition in a given block. `prefix *` will treat every top level definition in the same block above the statement as a prefix to all definitions below the statement.
11. `Encode t` means the current field is a string encoding of the enumeration object type `t`. For example, if we have `duck_reaction = Object ( quack | fly | swim )`, then `duck_reaction_type = Encode duck_reaction` means `duck_reaction_type = String ( "quack" | "fly" | "swim" )`

## Definitions

### Root

```haskell
data = {
  dir = String ( "request" | "response" ),
  signature,
  content_type = Encode content,
  content = Object ( account
                   | lab
                   | project
                   | seminar
                   | comment
                   -- | interaction -- maybe later for SNS
                   )
}
```

User signature

```haskell
prefix *

signature = {
  is_user = Boolean,     -- false means a guest
                         -- the following fields are valid if is_user == true
  user_email = String,   -- email format
  password_hash = String -- hash value format
}
```

### Account

```haskell
prefix data.content

account = {
  action = Encode data
  data = Object ( login
                | register
                | validate
                | reset_password
                | edit
                | delete
                | view
                | follow
                | unfollow
                )
}
```

#### Request

```haskell
when data.dir == "request"
prefix data.content.account.data

login = { }

-- data.signature.is_user == true in registering
register = { bio }

validate = {
  issue_new = Boolean,
  validation = String -- validation format
             -- empty: when issue_new == true, that is to send or resend an email
             -- non-empty: actual validation string
}

reset_password = { }

edit = { bio }

delete = { }

view = {
	lab = Boolean,
	project_create = Boolean,
	project_attend = Boolean,
  seminar_create = Boolean,
  seminar_attend = Boolean,
  comment = Boolean
} -- request to view a given account's view

follow = {
  person = user_email
}

unfollow = {
  person = user_email
}

```

#### Response

```haskell
when data.dir == "response"
prefix data.content.account.data

login = {
  status = Number ( 0 -- success
                  | 1 -- wrong password
                  | 2 -- account not found
                  | 3 -- missing JSON field
                  | 4 -- corrupted JSON
                  | 5 -- bad req/resp or content_type etc. in JSON
                  | 6 -- other failure
                  )
}

register = {
  status = Number ( 0 -- success
                  | 1 -- email or nickname already registered
                  | 2 -- invalid field (like date must be in "yyyy-mm-dd")
                  | 3 -- corrupted JSON
                  | 4 -- missing JSON field
                  | 5 -- bad req/resp or content_type etc. in JSON
                  | 6 -- other failure
                  )
}

validate = {
  status = Number ( 0 -- success
                  | 1 -- wrong validation
                  | 2 -- other failure
                  )
}

reset_password = {
  status = Number ( 0 -- success
                  | 1 -- no such account
                  | 2 -- other failure
                  )
}

reset_password = {
  status = Number ( 0 -- success
                  | 1 -- no such account
                  | 2 -- other failure
                  )
}

edit = {
  status = Number ( 0 -- success
									| 1 -- wrong password
									| 2 -- account not found
                  | 3 -- duplicated nickname
                  | 4 -- missing JSON field
                  | 5 -- corrupted JSON
                  | 6 -- bad req/resp or content_type etc. in JSON
                  | 7 -- other failure
                  )
}

delete = {
  status = Number ( 0 -- success
                  | 1 -- wrong password
                  | 2 -- account not found
                  | 3 -- missing JSON field
                  | 4 -- corrupted JSON
                  | 5 -- bad req/resp or content_type etc. in JSON
                  | 6 -- other failure
                  )
}

view = {
  status = Number ( 0 -- success
                  | 1 -- email or nickname already registered
                  | 2 -- invalid field (like date must be in "yyyy-mm-dd")
                  | 3 -- corrupted JSON
                  | 4 -- missing JSON field
                  | 5 -- bad req/resp or content_type etc. in JSON
                  | 6 -- other failure
                  ),
  bio
}

-- If the status number indicates one of the following
-- 		corrupted JSON
--		missing field
-- 		bad req/resp or content_type etc. in JSON
--		other failure
-- then the response JSON has the structure
-- {
--    "dir":"response",
--    "signature": { "is_user":false },
--    "content_type":"account",
--    "content":{
--            "action":"%s",
--            "data": { "status":%d }
--    }
-- }, where the action is filled according to the URL.
-- Otherwize, the signature field will be filled with the user's signature.



follow = { 
  status = Number (
                    0 -- success
                    1 -- no such person
                    2 -- already follow
                    3 -- already unfollow
                    4 -- login fail
                    5 -- corrupted JSON
                    6 -- other failure
                  )
}

unfollow = { 
  status = Number (
                    0 -- success
                    1 -- no such person
                    2 -- already follow
                    3 -- already unfollow
                    4 -- login fail
                    5 -- corrupted JSON
                    6 -- other failure
                  )
}
```

#### Common definitions

```haskell
prefix *

password_hash = String

bio = {
  real_name = String,
  nick_name = String,
  pic_url = String,         -- url format
  school = String,
  department = String,
  title = String,
  enrollment_date = String, -- date format
  -- when registering and editting, the following four fields need to be empty
  labs = [ lab_id = Number ], -- if the lab is on site
  projects_create = [ project_id = Number ],
  projects_attend = [ project_id = Number ],
  seminars_create = [ seminar_id = Number ],
  seminars_attend = [ seminar_id = Number ],
  comments = [ comment_id = Number ],
  profile = String          -- markdown format
}
```

### Lab

```haskell
prefix data.content

lab = {
  id = Number,  -- when creating, id == -1
  action = Encode data,
  data = Object ( create | edit | delete | view )
}
```

#### Request

```haskell
when data.dir == "request"
prefix data.content.lab.data

create = { lab_info }

edit = { lab_info }

delete = { }

view = { }
  
```

#### Response

```haskell
when data.dir == "response"
prefix data.content.lab.data

create = { status, id = Number }

edit = { status }

delete = { status }

view = {
  status = Number ( 0 -- success
                  | 1 -- no such lab
                  | 2 -- other failure
                  ),
  lab_info
}

status = Number ( 0 -- success
                | 1 -- invalid account
                | 2 -- permission denied
                | 3 -- other failure
                )

```

#### Common definitions

```haskell
prefix *

user_email = String -- email format

lab_info = {
  id = Number,  -- when creating, id == -1
  name = String,
  school = String,
  department = String,
  -- when creating, "", use upper definition
  owner_email = user_email,
  address = String,
  phone = String,          -- phone format
  front_page_url = String, -- url format
  pic_url = String,        -- url format, picture of members
  logo_url = String,       -- url format
  supervisors = String,
  comments = String,
  description = String,     -- markdown format
  create_date = String,     -- date format
	modified_date = String   -- date format
}

lab_bio = {
  name = String,
  school = String,
  department = String,
  title = String,
  pic_url = String,          -- url format
  is_user = Boolean,         -- if the person has an account
  -- the account can be obtained from here
  account_email = String ( ""         when is_user == false
                         | user_email when is_user == true
                         ),
  contact_email = String,    -- can be different from account_email
  address = String,
  profile = String           -- markdown format
}

```

### Project

```haskell
prefix data.content

project = {
  id = Number,  -- when creating, id == -1
  action = Encode data,
  data = Object ( create | edit | delete | view | join | drop | search )
}

```

#### Request

```haskell
when data.dir == "request"
prefix data.content.project.data

create = { project_info }

edit = { project_info }

delete = { }

view = { }

join = { }

drop = { }

getall = { }

search = {
	keywords = [ keyword = String ], -- keywords are used to intersect query results
	offset = Number, -- indicate the start number offset of query
	length = Number  -- inidcate the number of query results displayed
}

```

#### Response

```haskell
when data.dir == "response"
prefix data.content.project.data

create = { status, id = Number }

edit = { status }

delete = { status }

view = { status }

join = { status }

drop = { status }

getall = { 
  status = Number,
	projects = [ id = Number ],
	total_num = Number -- Total number of projects
}

search = {
	status = Number,
	ids = [ id = Number ], -- len(ids) == length (of query JSON)
	total_num = Number -- Total number of results, help frontend to determin offset and length
}

status = Number (
                  0 -- success
                  1 -- no project
                  2 -- project outdated
                  3 -- permission deny
                  4 -- user login fail
                  5 -- project quota is full 
                  6 -- user not in the project
                  7 -- json corrupt
                  8 -- project id error
                  9 -- user already in the project
                  10 -- other failure
                )

```

#### Common definitions

```haskell
prefix *

user_email = String -- email format

project_info = {
  id = Number,
  name = String,
  owner = user_email,
  start_date = String,  -- date format
  end_date = String,    -- date format
  member_total_need = Number,
  current_members = [ user_email ],
  comments = [ comment_id = Number ],
  description = String, -- markdown format
}

```

### Seminar

```haskell
prefix data.content

seminar = {
  id = Number,  -- when creating, id == -1
  action = Encode data,
  data = Object ( create | edit | delete | view | join | drop )
}

```

#### Request

```haskell
when data.dir == "request"
prefix data.content.seminar.data

create = { seminar_info }

edit = { seminar_info }

delete = { }

view = { }

join = { }

drop = { }

```

#### Response

```haskell
when data.dir == "response"
prefix data.content.seminar.data

create = { status, id = Number }

edit = { status }

delete = { status }

view = {
  status = Number ( 0 -- success
                  | 1 -- no such seminar
                  | 2 -- other failure
                  ),
  seminar_info
}

join = {
  status = Number ( 0 -- success
                  | 1 -- invalid account
                  | 2 -- already outdated
                  | 3 -- already full
                  | 4 -- other failure
                  )
}

drop = { status }

status = Number ( 0 -- success
                | 1 -- invalid account
                | 2 -- permission denied
                | 3 -- other failure
                )

```

#### Common definitions

```haskell
prefix *

user_email = String  -- email format

seminar_info = {
  id = Number,       -- when creating, id == -1
  name = String,
  owner = user_email,
  start_date = String,     -- date format
  end_date = String, -- date format
  member_number_limit = Number,
  current_members = [ user_email ],
  comments = [ comment_id = Number ],
  description = String -- markdown format
}

```

### Project Comment

```haskell
prefix data.content

comment = {
  id = Number,  -- when creating, id == project_id
  action = Encode data,
  data = Object ( comment_create | comment_edit | comment_delete | comment_view )
}

```

#### Request

```haskell
when data.dir == "request"
prefix data.content.comment.data

comment_create = {
  id = Number, -- seminar id
  description = String  -- markdown format
}

comment_edit = {
  comment_id = Number,
  description = String  -- markdown format
}

comment_delete = { 
  comment_id = Number
}

comment_view = {
  comment_id = Number
}

```

#### Response

```haskell
when data.dir == "response"
prefix data.content.comment.data

comment_create = { status, comment_id = Number }

comment_edit = { status, comment_id }

comment_delete = { status, comment_id }

comment_view = { status, comment_id }

status = Number ( 0 -- success
                | 1 -- other failure
                | 2 -- project outdated
                | 3 -- permission deny
                | 4 -- user login fail
                | 5 -- project quota is full 
                | 6 -- user not in the project
                | 7 -- json corrupt
                | 8 -- project id error
                | 9 -- user already in the project
                | 10 -- comment id error
                | 11 -- owner is trying to drop out of project
                )

```

### Generic Search

#### Request

```haskell
{
    "dir": "request",
    "content_type": "search",
    "content": {
        "keyword": String, --默认只检索标题是否含关键词
        "user_email": String, --以email限定指定用户发布的结果
        "user_type": "owner" | "attender", --这个用户在搜索结果里是参与者还是发布者
        "search_description": Boolean, --是否检索正文
        "search_lab": Boolean, --是否检索实验室信息
        "search_seminar": Boolean,
        "search_project": Boolean,
        "search_outdated": Boolean, --是否检索已经过期的project和seminar信息
        "curr_page": Number, --本次请求的页面号
    }
}

```

#### Response

```haskell
{
    "dir": "response",
    "content_type": "search",
    "status": Number,
    "content": {
        "total_results": Number, -- 搜索结果总数
        "last_page": Number, -- 搜索结果最后一页的页面号
        "result": [
            {
              "content_type": "lab" | "seminar" | "project",
              "id": Number 
            }
         ]
    }
}

status = ( 0 -- success
				 | 1 -- other error
				 | 2 -- bad json
				 )

```

