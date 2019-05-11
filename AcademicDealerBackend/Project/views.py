from django.http import HttpResponse
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
        return HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        return HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))

    # other unknown exceptions
    except Exception as e:
        print(e)
        return HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    # success
    return HttpResponse(gen_success_response(action, STATUS_SUCCESS, new_project.id))