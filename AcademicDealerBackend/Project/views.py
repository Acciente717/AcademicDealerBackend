from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import ProjectInfo, ProjectMember, UserAccount
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
            description = json_content_data['description'],
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
        project.description = json_content_data['description']

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
        print(project_id)
        project = ProjectInfo.objects.get(id=project_id)
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