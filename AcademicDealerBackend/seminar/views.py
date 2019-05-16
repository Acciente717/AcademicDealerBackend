from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from .models import SeminarInfo, SeminarMember, UserAccount, SeminarComment, LoginFail
from django.utils import timezone
import json
from .utils import *

def check_request(decoded, action):
    assert_dir(decoded, 'request')
    assert_content_type(decoded, 'seminar')
    assert_action(decoded, action)

def api_dispatch(request, url_action):
    dispatcher = {
        'create' : create,
        'edit' : edit,
        'delete' : delete,
        'view' : view,
        'join' : join,
        'drop' : drop,
        'search' : search,
        'getall' : getall
    }

    # return 404 when the url is invalid
    if url_action not in dispatcher:
        return HttpResponseNotFound()

    try:
        # decode JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)
        action = decoded['content']['action']
        if action != url_action:
            raise BadJSONType

        # dispatch to the handler
        http_resp = dispatcher[action](request)

    # bad JSON structure or missing field
    except (json.JSONDecodeError, BadJSONType, KeyError):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    # failed to login user
    except (LoginFail, UserAccount.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))

    # insufficient priviledge to delete
    except PermissionDenied:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))

    # seminar has already finished
    except SeminarOutdated:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OUTDATED))

    # user is already in the participant list
    except UserAlreadyIn:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_ALREADY_IN))
    
    # user is not in the seminar participant list
    except UserNotIn:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_NOT_IN))

    # seminar quota is full
    except SeminarAlreadyFull:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_ALREADY_FULL))

    # seminar ID is wrong or missing
    except (SeminarIDError, SeminarInfo.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_SEMINAR_ID_ERROR))
    
    # owner cannot join its own seminar
    except UserIsOwner:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_IS_OWNER))

    except Exception as e:
        print("Error: unknown exception at seminar dispatch!")
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def comment_api_dispatch(request, url_action):

    dispatcher = {
        'create' : comment_create,
        'edit' : comment_edit,
        'delete' : comment_delete,
        'view' : comment_view
    }

    # return 404 when the url is invalid
    if url_action not in dispatcher:
        return HttpResponseNotFound()

    try:
        # decode JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)
        action = decoded['content']['action']
        if action != 'comment_' + url_action:
            raise BadJSONType

        # dispatch to the handler
        http_resp = dispatcher[url_action](request)

    # bad JSON format
    except (json.JSONDecodeError, BadJSONType, KeyError):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_CORRUPTED_JSON))

    # insufficient priviledge
    except PermissionDenied:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PERMISSION_DENY))

    # invalid user
    except (LoginFail, UserAccount.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LOGIN_FAIL))

    # seminar ID error or missing
    except (SeminarIDError, SeminarInfo.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_SEMINAR_ID_ERROR))

    # comment ID error or missing
    except (CommentIDError, SeminarComment.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_COMMENT_ID_ERROR))

    # unknown error
    except Exception as e:
        print("Error: unknown exception at seminar comment dispatch!")
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp

def create(request):
    action = 'create'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'create')

    json_signature = decoded['signature']
    user = UserAccount.login(json_signature)

    json_content_data = decoded['content']['data']
    
    new_seminar = SeminarInfo(
        name = json_content_data['name'],
        owner = user,
        start_date = json_content_data['start_date'],
        end_date = json_content_data['end_date'],
        create_date = timezone.now(),
        modified_date = timezone.now(),
        member_number_limit = json_content_data['member_number_limit'],
        description = json_content_data['description'].replace('\n', '\\n')
    )
    new_seminar.save()

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, new_seminar.id))
    return http_resp

def edit(request):
    action = 'edit'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'edit')

    json_signature = decoded['signature']
    user = UserAccount.login(json_signature)

    json_content_data = decoded['content']['data']
    
    if "id" not in json_content_data:
        raise SeminarIDError
    
    seminar = SeminarInfo.objects.get(id=json_content_data['id'])

    if seminar.owner != user:
        raise PermissionDenied

    seminar.name = json_content_data['name']
    seminar.start_date = json_content_data['start_date']
    seminar.end_date = json_content_data['end_date']
    seminar.member_total_need = json_content_data['member_total_need']
    seminar.description = json_content_data['description'].replace('\n', '\\n')
    seminar.modified_date = timezone.now()
    seminar.save()

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, seminar.id))
    return http_resp

def delete(request):
    action = 'delete'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'delete')

    json_signature = decoded['signature']
    user = UserAccount.login(json_signature)

    json_content_data = decoded['content']['data']
    
    if "id" not in json_content_data:
        raise SeminarIDError
    
    seminar_id = json_content_data['id']
    seminar = SeminarInfo.objects.get(id=seminar_id)

    if seminar.owner != user:
        raise PermissionDenied

    seminar.delete()

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, seminar_id))
    return http_resp

def view(request):
    action = 'view'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'view')

    json_content_data = decoded['content']['data']
    
    if "id" not in json_content_data:
        raise SeminarIDError
    
    seminar_id = json_content_data['id']
    seminar = SeminarInfo.objects.get(id=seminar_id)

    members = repr([i.person.email for i in SeminarMember.objects.filter(seminar=seminar)])
    members = members.replace("'", '"')
    
    comments = repr([i.id for i in SeminarComment.objects.filter(seminar=seminar).order_by('modified_date')])

    response_msg = build_seminar_view(action, STATUS_SUCCESS, seminar_id, seminar, members, comments)

    http_resp = HttpResponse(response_msg)
    return http_resp

def getall(request):
    action = 'getall'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'getall')

    seminars = [i.id for i in SeminarInfo.objects.order_by('modified_date')]

    response_msg = build_seminar_list_view(action, STATUS_SUCCESS, seminars)

    http_resp = HttpResponse(response_msg)
    return http_resp

def join(request):
    action = 'join'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'join')

    json_signature = decoded['signature']
    user = UserAccount.login(json_signature)

    json_content_data = decoded['content']['data']
    
    if "id" not in json_content_data:
        raise SeminarIDError
    
    seminar_id = json_content_data['id']
    seminar = SeminarInfo.objects.get(id=seminar_id)

    if timezone.now() > seminar.end_date:
        raise SeminarOutdated

    members = [i.person for i in SeminarMember.objects.filter(seminar=seminar)]

    if user in members:
        raise UserAlreadyIn
    
    if user == seminar.owner:
        raise UserIsOwner
    
    seminar_member = SeminarMember(
        seminar = seminar,
        person = user,
    )
    seminar_member.save()
    
    if len(members) >= seminar.member_total_need:
        raise SeminarAlreadyFull

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, seminar.id))
    return http_resp

def drop(request):
    action = 'drop'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'drop')

    json_signature = decoded['signature']
    user = UserAccount.login(json_signature)

    json_content_data = decoded['content']['data']
    
    if "id" not in json_content_data:
        raise SeminarIDError
    
    seminar_id = json_content_data['id']
    seminar = SeminarInfo.objects.get(id=seminar_id)

    if timezone.now() > seminar.end_date:
        raise SeminarOutdated
    
    members = [i.person for i in SeminarMember.objects.filter(seminar=seminar)]

    if user not in members:
        raise UserNotIn
    
    seminar_member = SeminarMember.objects.get(
        seminar = seminar,
        person = user,
    )
    seminar_member.delete()
    
    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, seminar.id))
    return http_resp

def search(request):
    action = 'search'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, action)

    json_content_data = decoded['content']['data']

    query_sets = []
    for keyword in json_content_data['keywords']:
        query_sets.append(SeminarInfo.objects.filter(name__contains=keyword))
    query_sets = [set(i) for i in query_sets]
    intersected_query_result = set.intersection(*query_sets)
    
    response_ids = [i.id for i in intersected_query_result]

    resp = build_search_result(action, STATUS_SUCCESS, response_ids,
                                json_content_data['offset'],
                                json_content_data['offset'] + json_content_data['length'])

    http_resp = HttpResponse(resp)
    return http_resp

def comment_create(request):
    action = 'comment_create'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'comment_create')

    json_signature = decoded['signature']
    user = UserAccount.login(json_signature)

    json_content_data = decoded['content']['data']
    
    if "id" not in json_content_data:
        raise SeminarIDError
    
    seminar = SeminarInfo.objects.get(id=json_content_data['id'])

    seminar.modified_date = timezone.now()
    seminar.save()

    seminar_comment = SeminarComment(
        seminar = seminar,
        owner = user,
        create_date = timezone.now(),
        modified_date = timezone.now(),
        description = json_content_data['description']
    )
    seminar_comment.save()

    http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, seminar_comment.id))
    return http_resp

def comment_edit(request):
    action = 'comment_edit'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'comment_edit')

    json_signature = decoded['signature']
    user = UserAccount.login(json_signature)

    json_content_data = decoded['content']['data']
    
    if "comment_id" not in json_content_data:
        raise CommentIDError
    
    seminar_comment = SeminarComment.objects.get(id=json_content_data['comment_id'])

    if seminar_comment.owner != user:
        raise PermissionDenied

    seminar_comment.modified_date = timezone.now()
    seminar_comment.description = json_content_data['description'].replace('\n', '\\n')
    seminar_comment.save()

    seminar = seminar_comment.seminar
    seminar.modified_date = timezone.now()
    seminar.save()

    http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, seminar_comment.id))
    return http_resp

def comment_delete(request):
    action = 'comment_delete'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'comment_delete')

    json_signature = decoded['signature']
    user = UserAccount.login(json_signature)

    json_content_data = decoded['content']['data']
    
    if "comment_id" not in json_content_data:
        raise CommentIDError
    
    comment_id = json_content_data['comment_id']
    seminar_comment = SeminarComment.objects.get(id=comment_id)

    if seminar_comment.owner != user:
        raise PermissionDenied

    seminar_comment.delete()

    http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, comment_id))
    return http_resp

def comment_view(request):
    action = 'comment_view'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'comment_view')

    json_content_data = decoded['content']['data']
    
    if "comment_id" not in json_content_data:
        raise CommentIDError
    
    comment_id = json_content_data['comment_id']
    seminar_comment = SeminarComment.objects.get(id=comment_id)

    response_msg = build_comment_view(action, STATUS_SUCCESS, comment_id, seminar_comment)

    http_resp = HttpResponse(response_msg)
    return http_resp
