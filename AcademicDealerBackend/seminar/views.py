from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import SeminarInfo, SeminarMember, UserAccount
from django.utils import timezone
from datetime import datetime
import json
from .utils import *

def check_request(decoded, action):
    assert_dir(decoded, 'request')
    assert_content_type(decoded, 'seminar')
    assert_action(decoded, action)

def create(request):
    action = 'create'

    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        check_request(decoded, 'create')

        # login user
        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        # create new seminar
        json_content_data = decoded['content']['data']
        new_seminar = SeminarInfo(
            name = json_content_data['name'],
            owner = user,
            start_date = json_content_data['start_date'],
            end_date = json_content_data['end_date'],
            member_number_limit = json_content_data['member_number_limit'],
            description = json_content_data['description'].replace('\n', '\\n')
        )
        new_seminar.save()

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
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, new_seminar.id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def edit(request):
    action = 'edit'

    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        check_request(decoded, 'edit')

        # login user
        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        # update seminar info
        json_content_data = decoded['content']['data']

        if "id" not in json_content_data:
            raise SeminarIDError

        seminar = SeminarInfo.objects.get(id=json_content_data['id'])

        if seminar.owner != user:
            raise PermissionDenied

        seminar.name = json_content_data['name']
        seminar.start_date = json_content_data['start_date']
        seminar.end_date = json_content_data['end_date']
        seminar.member_number_limit = json_content_data['member_number_limit']
        seminar.description = json_content_data['description'].replace('\n', '\\n')

        seminar.save()

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except PermissionDenied:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))
    
    except (SeminarIDError, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, seminar.id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def delete(request):
    action = 'delete'

    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        check_request(decoded, 'delete')

        # login user
        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        # delete seminar
        json_content_data = decoded['content']['data']
        
        if "id" not in json_content_data:
            raise SeminarIDError

        seminar_id = json_content_data['id']
        seminar = SeminarInfo.objects.get(id=seminar_id)

        if seminar.owner != user:
            raise PermissionDenied

        seminar.delete()

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except PermissionDenied:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))
    
    except (SeminarIDError, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, seminar_id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def view(request):
    action = 'view'

    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        check_request(decoded, 'view')

        # build JSON response
        json_content_data = decoded['content']['data']

        if "id" not in json_content_data:
            raise SeminarIDError

        seminar_id = json_content_data['id']
        seminar = SeminarInfo.objects.get(id=seminar_id)

        members = repr([i.person.email for i in SeminarMember.objects.filter(seminar=seminar)])
        members = members.replace("'", '"')

        response_msg = build_seminar_view(action, STATUS_SUCCESS, seminar_id, seminar, members)

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))

    except PermissionDenied:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))

    except (SeminarIDError, ObjectDoesNotExist):
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
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        check_request(decoded, 'join')

        # login user
        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        # join seminar
        json_content_data = decoded['content']['data']

        if "id" not in json_content_data:
            raise SeminarIDError

        seminar_id = json_content_data['id']
        seminar = SeminarInfo.objects.get(id=seminar_id)

        if timezone.now() > seminar.end_date:
            raise SeminarOutDated

        members = [i.person for i in SeminarMember.objects.filter(seminar=seminar)]

        if user in members:
            raise UserAlreadyIn

        seminar_member = SeminarMember(
            seminar = seminar,
            person = user,
        )
        seminar_member.save()

        if len(members) >= seminar.member_number_limit:
            raise SeminarAlreadyFull

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))

    except PermissionDenied:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))

    except SeminarOutDated:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OUTDATED))

    except UserAlreadyIn:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_ALREADY_IN))

    except SeminarAlreadyFull:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_ALREADY_FULL))

    except (SeminarIDError, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, seminar.id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def drop(request):
    action = 'drop'

    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        check_request(decoded, 'drop')

        # login user
        json_signature = decoded['signature']
        if json_signature['is_user'] != True:
            raise LoginFail
        user = UserAccount.objects.get(email=json_signature['user_email'])
        if user.pw_hash != json_signature['password_hash']:
            raise LoginFail

        # drop seminar
        json_content_data = decoded['content']['data']

        if "id" not in json_content_data:
            raise SeminarIDError

        seminar_id = json_content_data['id']
        seminar = SeminarInfo.objects.get(id=seminar_id)

        if timezone.now() > seminar.end_date:
            raise SeminarOutDated

        members = [i.person for i in SeminarMember.objects.filter(seminar=seminar)]

        if user not in members:
            raise UserNotIn

        seminar_member = SeminarMember.objects.get(
            seminar = seminar,
            person = user,
        )
        seminar_member.delete()

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except PermissionDenied:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))
    
    except SeminarOutDated:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OUTDATED))
    
    except UserNotIn:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_NOT_IN))
    
    except (SeminarIDError, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, seminar.id))


    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def search(request):
    action = 'search'

    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        check_request(decoded, action)

        json_content_data = decoded['content']['data']

        # search seminar
        query_sets = []
        for keyword in json_content_data['keywords']:
            query_sets.append(SeminarInfo.objects.filter(name__contains=keyword))
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
            raise SeminarIDError
        
        seminar = SeminarInfo.objects.get(id=json_content_data['id'])

        comment = Comment(
            seminar = seminar,
            owner = user,
            modified_date = datetime.now(),
            description = json_content_data['description']
        )
        comment.save()

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    except LoginFail:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))
    
    except (SeminarIDError, ObjectDoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # other unknown exceptions
    except Exception as e:
        print("error", e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    else:
    # success
        http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, comment.id))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp
