from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from .models import ProjectInfo, ProjectMember, UserAccount, ProjectComment, LoginFail
from django.utils import timezone
from django.db import transaction
import json
from .utils import *


def check_request(decoded, action):
    assert_dir(decoded, 'request')
    assert_content_type(decoded, 'project')
    assert_action(decoded, action)


def api_dispatch(request, url_action):
    dispatcher = {
        'create': create,
        'edit': edit,
        'delete': delete,
        'view': view,
        'join': join,
        'drop': drop,
        'search': search,
        'getall': getall
    }

    action = "unknown action"

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

    # project has already finished
    except ProjectOutdated:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OUTDATED))

    # user is already in the participant list
    except UserAlreadyIn:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_ALREADY_IN))

    # user is not in the project participant list
    except UserNotIn:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_NOT_IN))

    # project quota is full
    except ProjectAlreadyFull:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_ALREADY_FULL))

    # project ID is wrong or missing
    except (ProjectIDError, ProjectInfo.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # project owner is trying to drop out
    except UserIsOwner:
        http_resp = HttpResponse(gen_fail_response(action, STATUS_IS_OWNER))

    except Exception as e:
        print("Error: unknown exception at project dispatch!")
        print(e)
        http_resp = HttpResponse(gen_fail_response(action, STATUS_OTHER_FAILURE))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp


def comment_api_dispatch(request, url_action):
    dispatcher = {
        'create': comment_create,
        'edit': comment_edit,
        'delete': comment_delete,
        'view': comment_view
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

    # project ID error or missing
    except (ProjectIDError, ProjectInfo.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_PROJECT_ID_ERROR))

    # comment ID error or missing
    except (CommentIDError, ProjectComment.DoesNotExist):
        http_resp = HttpResponse(gen_fail_response(action, STATUS_COMMENT_ID_ERROR))

    # unknown error
    except Exception as e:
        print("Error: unknown exception at project comment dispatch!")
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

    new_project = ProjectInfo(
        name=json_content_data['name'],
        owner=user,
        start_date=json_content_data['start_date'],
        end_date=json_content_data['end_date'],
        create_date=timezone.now(),
        modified_date=timezone.now(),
        member_total_need=json_content_data['member_total_need'],
        description=json_content_data['description']
    )
    new_project.save()

    project_member = ProjectMember(
        project=new_project,
        person=user,
    )
    project_member.save()

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, new_project.id))
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
        raise ProjectIDError

    project = ProjectInfo.objects.get(id=json_content_data['id'])

    if project.owner != user:
        raise PermissionDenied

    project.name = json_content_data['name']
    project.start_date = json_content_data['start_date']
    project.end_date = json_content_data['end_date']
    project.member_total_need = json_content_data['member_total_need']
    project.description = json_content_data['description']
    project.modified_date = timezone.now()
    project.save()

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, project.id))
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
        raise ProjectIDError

    project_id = json_content_data['id']
    project = ProjectInfo.objects.get(id=project_id)

    if project.owner != user:
        raise PermissionDenied

    project.delete()

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, project_id))
    return http_resp


def view(request):
    action = 'view'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'view')

    json_content_data = decoded['content']['data']

    if "id" not in json_content_data:
        raise ProjectIDError

    project_id = json_content_data['id']
    project = ProjectInfo.objects.get(id=project_id)

    members = [i.person.email for i in ProjectMember.objects.filter(project=project)]

    comments = [i.id for i in ProjectComment.objects.filter(project=project).order_by('modified_date')]

    response_msg = build_project_view(action, STATUS_SUCCESS, project_id, project, members, comments)

    http_resp = HttpResponse(response_msg)
    return http_resp


def getall(request):
    action = 'getall'

    body = str(request.body, encoding='utf8')
    decoded = json.loads(body)

    check_request(decoded, 'getall')

    projects = [i.id for i in ProjectInfo.objects.order_by('modified_date')]

    response_msg = build_project_list_view(action, STATUS_SUCCESS, projects)

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
        raise ProjectIDError

    project_id = json_content_data['id']
    project = ProjectInfo.objects.get(id=project_id)

    if timezone.now() > project.end_date:
        raise ProjectOutdated

    members = [i.person for i in ProjectMember.objects.filter(project=project)]

    if user in members:
        raise UserAlreadyIn

    project_member = ProjectMember(
        project=project,
        person=user,
    )
    project_member.save()

    if len(members) >= project.member_total_need:
        raise ProjectAlreadyFull

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, project.id))
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
        raise ProjectIDError

    project_id = json_content_data['id']
    project = ProjectInfo.objects.get(id=project_id)

    if timezone.now() > project.end_date:
        raise ProjectOutdated

    members = [i.person for i in ProjectMember.objects.filter(project=project)]

    if user not in members:
        raise UserNotIn

    if user == project.owner:
        raise UserIsOwner

    project_member = ProjectMember.objects.get(
        project=project,
        person=user,
    )
    project_member.delete()

    http_resp = HttpResponse(gen_success_response(action, STATUS_SUCCESS, project.id))
    return http_resp


def search(request):
    action = 'search'

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
        raise ProjectIDError

    project = ProjectInfo.objects.get(id=json_content_data['id'])

    project.modified_date = timezone.now()
    project.save()

    project_comment = ProjectComment(
        project=project,
        owner=user,
        create_date=timezone.now(),
        modified_date=timezone.now(),
        description=json_content_data['description']
    )
    project_comment.save()

    http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, project_comment.id))
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

    project_comment = ProjectComment.objects.get(id=json_content_data['comment_id'])

    if project_comment.owner != user:
        raise PermissionDenied

    project_comment.modified_date = timezone.now()
    project_comment.description = json_content_data['description']
    project_comment.save()

    project = project_comment.project
    project.modified_date = timezone.now()
    project.save()

    http_resp = HttpResponse(gen_success_response_comment(action, STATUS_SUCCESS, project_comment.id))
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
    project_comment = ProjectComment.objects.get(id=comment_id)

    if project_comment.owner != user:
        raise PermissionDenied

    project_comment.delete()

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
    project_comment = ProjectComment.objects.get(id=comment_id)

    response_msg = build_comment_view(action, STATUS_SUCCESS, comment_id, project_comment)

    http_resp = HttpResponse(response_msg)
    return http_resp
