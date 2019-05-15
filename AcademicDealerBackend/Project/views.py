from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import ProjectInfo, ProjectMember, UserAccount, Comment
from django.utils import timezone
import json
from .utils import *

def check_request(decoded, action):
    assert_dir(decoded, 'request')
    assert_content_type(decoded, 'project')
    assert_action(decoded, action)

def create(request):
    action = 'create'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, 'create')

        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        json_content_data = decoded['content']['data']
        
        new_project = ProjectInfo(
            name = json_content_data['name'],
            owner = user,
            start_date = json_content_data['start_date'],
            end_date = json_content_data['end_date'],
            member_total_need = json_content_data['member_total_need'],
            description = json_content_data['description'].replace('\n', '\\n')
        )
        new_project.save()

        project_member = ProjectMember(
            project = new_project,
            person = user,
        )
        project_member.save()

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, new_project.id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def edit(request):
    action = 'edit'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, 'edit')

        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        json_content_data = decoded['content']['data']
        
        if "id" not in json_content_data:
            raise PROJECT_ID_ERROR
        
        project = ProjectInfo.objects.get(id=json_content_data['id'])

        if project.owner != user:
            raise PERMISSION_DENY

        project.name = json_content_data['name']
        project.start_date = json_content_data['start_date']
        project.end_date = json_content_data['end_date']
        project.member_total_need = json_content_data['member_total_need']
        project.description = json_content_data['description'].replace('\n', '\\n')

        project.save()

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except PERMISSION_DENY:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))
    
    except (PROJECT_ID_ERROR, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, project.id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def delete(request):
    action = 'delete'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, 'delete')

        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        json_content_data = decoded['content']['data']
        
        if "id" not in json_content_data:
            raise PROJECT_ID_ERROR
        
        project_id = json_content_data['id']
        project = ProjectInfo.objects.get(id=project_id)

        if project.owner != user:
            raise PERMISSION_DENY

        project.delete()

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except PERMISSION_DENY:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))
    
    except (PROJECT_ID_ERROR, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, project_id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def view(request):
    action = 'view'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, 'view')

        json_content_data = decoded['content']['data']
        
        if "id" not in json_content_data:
            raise PROJECT_ID_ERROR
        
        project_id = json_content_data['id']
        project = ProjectInfo.objects.get(id=project_id)

        members = repr([i.person.email for i in ProjectMember.objects.filter(project=project)])
        members = members.replace("'", '"')
        
        comments = repr([i.id for i in Comment.objects.filter(project=project)])
        comments = comments.replace("'", '"')

        response_msg = build_project_view(action, STATUS_SUCCESS, project_id, project, members, comments)

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except (PROJECT_ID_ERROR, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(response_msg)

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def join(request):
    action = 'join'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, 'join')

        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        json_content_data = decoded['content']['data']
        
        if "id" not in json_content_data:
            raise PROJECT_ID_ERROR
        
        project_id = json_content_data['id']
        project = ProjectInfo.objects.get(id=project_id)

        if timezone.now() > project.end_date:
            raise OUTDATE
        
        members = [i.person for i in ProjectMember.objects.filter(project=project)]

        if user in members:
            raise ALREADY_IN
        
        project_member = ProjectMember(
            project = project,
            person = user,
        )
        project_member.save()
        
        if len(members) >= project.member_total_need:
            raise ALREADY_FULL

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except PERMISSION_DENY:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))
    
    except OUTDATE:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OUTDATED))
    
    except ALREADY_IN:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_ALREADY_IN))
    
    except ALREADY_FULL:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_ALREADY_FULL))
    
    except (PROJECT_ID_ERROR, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, project.id))


    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def drop(request):
    action = 'drop'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, 'drop')

        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        json_content_data = decoded['content']['data']
        
        if "id" not in json_content_data:
            raise PROJECT_ID_ERROR
        
        project_id = json_content_data['id']
        project = ProjectInfo.objects.get(id=project_id)

        if timezone.now() > project.end_date:
            raise OUTDATE
        
        members = [i.person for i in ProjectMember.objects.filter(project=project)]

        if user not in members:
            raise NOT_IN
        
        project_member = ProjectMember.objects.get(
            project = project,
            person = user,
        )
        project_member.delete()
        
    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except PERMISSION_DENY:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))
    
    except OUTDATE:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OUTDATED))
    
    except NOT_IN:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_NOT_IN))
    
    except (PROJECT_ID_ERROR, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, project.id))


    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def search(request):
    action = 'search'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, action)

        json_content_data = decoded['content']['data']

        query_sets = []
        for keyword in json_content_data['keywords']:
            query_sets.append(ProjectInfo.objects.filter(name__contains=keyword))
        query_sets = [set(i) for i in query_sets]
        intersected_query_result = set.intersection(*query_sets)
        
        response_ids = [i.id for i in intersected_query_result]

        resp = build_search_result(action, STATUS_SUCCESS, response_ids,
                                   json_content_data['offset'],
                                   json_content_data['length'])

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
        http_resp = HttpResponse(resp)
    
    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def comment_create(request):
    action = 'comment_create'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, 'comment_create')

        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        json_content_data = decoded['content']['data']
        
        if "id" not in json_content_data:
            raise PROJECT_ID_ERROR
        
        project = ProjectInfo.objects.get(id=json_content_data['id'])

        comment = Comment(
            project = project,
            owner = user,
            create_date = timezone.now(),
            modified_date = timezone.now(),
            description = json_content_data['description']
        )
        comment.save()

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except (PROJECT_ID_ERROR, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print("error", e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, comment.id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def comment_edit(request):
    action = 'comment_edit'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, 'comment_edit')

        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        json_content_data = decoded['content']['data']
        
        if "comment_id" not in json_content_data:
            raise COMMENT_ID_ERROR
        
        comment = Comment.objects.get(id=json_content_data['comment_id'])

        if comment.owner != user:
            raise PERMISSION_DENY

        comment.modified_date = timezone.now()
        comment.description = json_content_data['description'].replace('\n', '\\n')
        comment.save()

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except (COMMENT_ID_ERROR, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_COMMENT_ID_ERROR))

    except PERMISSION_DENY:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))

    # other unknown exceptions
    except Exception as e:
        print("error", e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, comment.id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def comment_delete(request):
    action = 'comment_delete'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, 'comment_delete')

        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        json_content_data = decoded['content']['data']
        
        if "comment_id" not in json_content_data:
            raise COMMENT_ID_ERROR
        
        comment_id = json_content_data['comment_id']
        comment = Comment.objects.get(id=comment_id)

        if comment.owner != user:
            raise PERMISSION_DENY

        comment.delete()

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except (COMMENT_ID_ERROR, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_COMMENT_ID_ERROR))

    except PERMISSION_DENY:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))

    # other unknown exceptions
    except Exception as e:
        print("error", e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, comment_id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def comment_view(request):
    action = 'comment_view'

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        check_request(decoded, 'comment_view')

        json_content_data = decoded['content']['data']
        
        if "comment_id" not in json_content_data:
            raise COMMENT_ID_ERROR
        
        comment_id = json_content_data['comment_id']
        comment = Comment.objects.get(id=comment_id)

        response_msg = build_comment_view(action, STATUS_SUCCESS, comment_id, comment)
        
    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except (COMMENT_ID_ERROR, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_COMMENT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print("error", e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(response_msg)

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp