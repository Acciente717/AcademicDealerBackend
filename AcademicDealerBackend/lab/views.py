from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from .models import LabInfo, UserAccount, LabComment, LoginFail
from django.utils import timezone
from django.db import transaction
import json
from .utils import *

def check_request(decoded, action):
    assert_dir(decoded, 'request')
    assert_content_type(decoded, 'lab')
    assert_action(decoded, action)

def api_dispatch(request, url_action):
    dispatcher = {
        'create' : create,
        'edit' : edit,
        'delete' : delete,
        'view' : view,
        'search' : search,
        'getall' : getall
    }

    # return 404 when the url is invalid
    if url_action not in dispatcher:
        return HttpResponseNotFound()

    try:
        with transaction.atomic():
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

    # lab ID is wrong or missing
    except (LabIDError, LabInfo.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LAB_ID_ERROR))

    except Exception as e:
        print("Error: unknown exception at lab dispatch!")
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
        with transaction.atomic():
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

    # lab ID error or missing
    except (LabIDError, LabInfo.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_LAB_ID_ERROR))

    # comment ID error or missing
    except (CommentIDError, LabComment.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_COMMENT_ID_ERROR))

    # unknown error
    except Exception as e:
        print("Error: unknown exception at lab comment dispatch!")
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
    
    new_lab = LabInfo(
        name = json_content_data['name'],
        school = json_content_data['school'],
        department = json_content_data['department'],
        owner = user,
        address = json_content_data['address'],
        phone = json_content_data['phone'],
        front_page_url = json_content_data['front_page_url'],
        pic_url = json_content_data['pic_url'],
        logo_url = json_content_data['logo_url'],
        supervisors = json_content_data['supervisors'],
        create_date = timezone.now(),
        modified_date = timezone.now(),
        description = json_content_data['description']
    )

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, new_lab.id))
    new_lab.save()

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
        raise LabIDError
    
    lab = LabInfo.objects.get(id=json_content_data['id'])

    if lab.owner != user:
        raise PermissionDenied


    lab.name = json_content_data['name'],
    lab.school = json_content_data['school'],
    lab.department = json_content_data['department'],
    lab.address = json_content_data['address'],
    lab.phone = json_content_data['phone'],
    lab.front_page_url = json_content_data['front_page_url'],
    lab.pic_url = json_content_data['pic_url'],
    lab.logo_url = json_content_data['logo_url'],
    lab.supervisors = json_content_data['supervisors'],
    lab.modified_date = timezone.now(),
    lab.description = json_content_data['description']

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, lab.id))
    lab.save()

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
        raise LabIDError
    
    lab_id = json_content_data['id']
    lab = LabInfo.objects.get(id=lab_id)

    if lab.owner != user:
        raise PermissionDenied

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, lab_id))
    lab.delete()

    return http_resp

def view(request):
    action = 'view'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'view')

    json_content_data = decoded['content']['data']
    
    if "id" not in json_content_data:
        raise LabIDError
    
    lab_id = json_content_data['id']
    lab = LabInfo.objects.get(id=lab_id)
    
    comments = [i.id for i in LabComment.objects.filter(lab=lab).order_by('modified_date')]

    response_msg = build_lab_view(action, STATUS_SUCCESS, lab_id, lab, comments)

    http_resp = HttpResponse(response_msg)
    return http_resp

def getall(request):
    action = 'getall'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'getall')

    labs = [i.id for i in LabInfo.objects.order_by('modified_date')]

    response_msg = build_lab_list_view(action, STATUS_SUCCESS, labs)

    http_resp = HttpResponse(response_msg)
    return http_resp

def search(request):
    action = 'search'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, action)

    json_content_data = decoded['content']['data']

    query_sets = []
    for keyword in json_content_data['keywords']:
        query_sets.append(LabInfo.objects.filter(name__contains=keyword))
    query_sets = [set(i) for i in query_sets]
    intersected_query_result = set.intersection(*query_sets)
    
    response_ids = [i.id for i in intersected_query_result]

    resp = build_search_result(action, STATUS_SUCCESS, response_ids,
                                json_content_data['offset'],
                                json_content_data['length'])

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
        raise LabIDError
    
    lab = LabInfo.objects.get(id=json_content_data['id'])

    lab.modified_date = timezone.now()

    lab_comment = LabComment(
        lab = lab,
        owner = user,
        create_date = timezone.now(),
        modified_date = timezone.now(),
        description = json_content_data['description']
    )

    http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, lab_comment.id))
    lab_comment.save()
    lab.save()

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
    
    lab_comment = LabComment.objects.get(id=json_content_data['comment_id'])

    if lab_comment.owner != user:
        raise PermissionDenied

    lab_comment.modified_date = timezone.now()
    lab_comment.description = json_content_data['description']

    lab = lab_comment.lab
    lab.modified_date = timezone.now()

    http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, lab_comment.id))
    lab_comment.save()
    lab.save()

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
    lab_comment = LabComment.objects.get(id=comment_id)

    if lab_comment.owner != user:
        raise PermissionDenied

    http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, comment_id))
    lab_comment.delete()

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
    lab_comment = LabComment.objects.get(id=comment_id)

    response_msg = build_comment_view(action, STATUS_SUCCESS, comment_id, lab_comment)

    http_resp = HttpResponse(response_msg)
    return http_resp
