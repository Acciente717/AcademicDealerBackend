from django.shortcuts import render
from .models import UserAccount, UserFollow, LoginFail
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import json
from Project.models import ProjectInfo, ProjectMember
from .utils import *


def register(request):
    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        assert_dir(decoded, 'request')
        assert_content_type(decoded, 'account')
        assert_account_action(decoded, 'register')

        # create new user
        json_signature = decoded['signature']
        json_content_data = decoded['content']['data']
        new_user = UserAccount(
            email=json_signature['user_email'],
            pw_hash=json_signature['password_hash'],
            real_name=json_content_data['real_name'],
            nick_name=json_content_data['nick_name'],
            pic_url=json_content_data['pic_url'],
            school=json_content_data['school'],
            department=json_content_data['department'],
            title=json_content_data['title'],
            enrollment_date=json_content_data['enrollment_date'],
            profile=json_content_data['profile'].replace('\n', '\\n')
        )
        new_user.save()

    # bad JSON format
    except json.JSONDecodeError:
        http_resp = HttpResponse(gen_register_fail(None, REGISTER_CORRUPTED_JSON))

    # duplicated email or nickname
    except IntegrityError:
        http_resp = HttpResponse(gen_register_fail(decoded, REGISTER_DUPLICATE_MAIL_NICKNAME))

    # wrong format of specific fields
    # for example, date must be in "yyyy-mm-dd"
    except ValidationError:
        http_resp = HttpResponse(gen_register_fail(decoded, REGISTER_INVALID_FIELD))

    # missing json fields
    except KeyError:
        http_resp = HttpResponse(gen_register_fail(decoded, REGISTER_MISSING_FIELD))

    # bad json type
    except BadJSONType:
        http_resp = HttpResponse(gen_register_fail(decoded, REGISTER_BAD_TYPE))

    # other unknown exceptions
    except Exception:
        http_resp = HttpResponse(gen_register_fail(decoded, REGISTER_OTHER_ERROR))

    # success
    else:
        http_resp = HttpResponse(gen_register_success(decoded))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp


def login(request):
    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        assert_dir(decoded, 'request')
        assert_content_type(decoded, 'account')
        assert_account_action(decoded, 'login')

        # search database and compare password
        user = UserAccount.objects.get(email=decoded['signature']['user_email'])
        if user.pw_hash != decoded['signature']['password_hash']:
            raise BadPassword

    # wrong password
    except BadPassword:
        http_resp = HttpResponse(gen_login_fail(decoded, LOGIN_WRONG_PASSWORD))

    # email not found
    except UserAccount.DoesNotExist:
        http_resp = HttpResponse(gen_login_fail(decoded, LOGIN_EMAIL_NOT_FOUND))

    # bad JSON format
    except json.JSONDecodeError:
        http_resp = HttpResponse(gen_login_fail(None, LOGIN_CORRUPTED_JSON))

    # missing json fields
    except KeyError:
        http_resp = HttpResponse(gen_login_fail(decoded, LOGIN_MISSING_FIELD))

    # bad json type
    except BadJSONType:
        http_resp = HttpResponse(gen_login_fail(decoded, LOGIN_BAD_TYPE))

    # other unknown exceptions
    except Exception:
        http_resp = HttpResponse(gen_login_fail(decoded, LOGIN_OTHER_ERROR))

    # success
    else:
        http_resp = HttpResponse(gen_login_success(decoded))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp


def view(request):
    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        assert_dir(decoded, 'request')
        assert_content_type(decoded, 'account')
        assert_account_action(decoded, 'view')

        # search database
        user = UserAccount.objects.get(email=decoded['signature']['user_email'])
        labs = []
        projects_create = [i.id for i in ProjectInfo.objects.filter(owner=user.id)] \
            if decoded['content']['data']['project_create'] else []
        projects_attend = [i.project.id for i in ProjectMember.objects.filter(person=user.id)] \
            if decoded['content']['data']['project_attend'] else []
        seminars_create = []
        seminars_attend = []
        comments = []

        follows = [i.follow_user.email for i in UserFollow.objects.filter(user=user)]
        follow_by = [i.user.email for i in UserFollow.objects.filter(follow_user=user)]

        # build response JSON
        resp = build_user_bio_json(user, labs, projects_create, projects_attend,
                                   seminars_create, seminars_attend, comments, follows, follow_by)

    # email not found
    except UserAccount.DoesNotExist:
        http_resp = HttpResponse(gen_view_fail(decoded, VIEW_EMAIL_NOT_FOUND))

    # bad JSON format
    except json.JSONDecodeError:
        http_resp = HttpResponse(gen_view_fail(None, VIEW_CORRUPTED_JSON))

    # missing json fields
    except KeyError:
        http_resp = HttpResponse(gen_view_fail(decoded, VIEW_MISSING_FIELD))

    # bad json type
    except BadJSONType:
        http_resp = HttpResponse(gen_view_fail(decoded, VIEW_BAD_TYPE))

    # other unknown exceptions
    except Exception:
        http_resp = HttpResponse(gen_view_fail(decoded, VIEW_OTHER_ERROR))

    # success
    else:
        http_resp = HttpResponse(resp)

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp


def edit(request):
    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        assert_dir(decoded, 'request')
        assert_content_type(decoded, 'account')
        assert_account_action(decoded, 'edit')

        # search database and compare password
        json_content_data = decoded['content']['data']
        user = UserAccount.objects.get(email=decoded['signature']['user_email'])
        if user.pw_hash != decoded['signature']['password_hash']:
            raise BadPassword

        # update user biography
        user.real_name = json_content_data['real_name']
        user.nick_name = json_content_data['nick_name']
        user.pic_url = json_content_data['pic_url']
        user.school = json_content_data['school']
        user.department = json_content_data['department']
        user.title = json_content_data['title']
        user.enrollment_date = json_content_data['enrollment_date']
        user.profile = json_content_data['profile'].replace('\n', '\\n')
        user.save()

    # duplicated new nickname
    except IntegrityError:
        http_resp = HttpResponse(gen_edit_fail(decoded, EDIT_DUPLICATED_NICKNAME))

    # wrong password
    except BadPassword:
        http_resp = HttpResponse(gen_edit_fail(decoded, EDIT_WRONG_PASSWORD))

    # email not found
    except UserAccount.DoesNotExist:
        http_resp = HttpResponse(gen_edit_fail(decoded, EDIT_EMAIL_NOT_FOUND))

    # bad JSON format
    except json.JSONDecodeError:
        http_resp = HttpResponse(gen_edit_fail(None, EDIT_CORRUPTED_JSON))

    # wrong format of specific fields
    # for example, date must be in "yyyy-mm-dd"
    except ValidationError:
        http_resp = HttpResponse(gen_edit_fail(decoded, EDIT_INVALID_FIELD))

    # missing json fields
    except KeyError:
        http_resp = HttpResponse(gen_edit_fail(decoded, EDIT_MISSING_FIELD))

    # bad json type
    except BadJSONType:
        http_resp = HttpResponse(gen_edit_fail(decoded, EDIT_BAD_TYPE))

    # other unknown exceptions
    except Exception:
        http_resp = HttpResponse(gen_edit_fail(decoded, EDIT_OTHER_ERROR))

    # success
    else:
        http_resp = HttpResponse(gen_edit_success(decoded))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp


def delete(request):
    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        assert_dir(decoded, 'request')
        assert_content_type(decoded, 'account')
        assert_account_action(decoded, 'delete')

        # search database and compare password
        user = UserAccount.objects.get(email=decoded['signature']['user_email'])
        if user.pw_hash != decoded['signature']['password_hash']:
            raise BadPassword

        # delete user
        user.delete()

    # wrong password
    except BadPassword:
        http_resp = HttpResponse(gen_delete_fail(decoded, DELETE_WRONG_PASSWORD))

    # email not found
    except UserAccount.DoesNotExist:
        http_resp = HttpResponse(gen_delete_fail(decoded, DELETE_EMAIL_NOT_FOUND))

    # bad JSON format
    except json.JSONDecodeError:
        http_resp = HttpResponse(gen_delete_fail(None, DELETE_CORRUPTED_JSON))

    # missing json fields
    except KeyError:
        http_resp = HttpResponse(gen_delete_fail(decoded, DELETE_MISSING_FIELD))

    # bad json type
    except BadJSONType:
        http_resp = HttpResponse(gen_delete_fail(decoded, DELETE_BAD_TYPE))

    # other unknown exceptions
    except Exception:
        http_resp = HttpResponse(gen_delete_fail(decoded, DELETE_OTHER_ERROR))

    # success
    else:
        http_resp = HttpResponse(gen_delete_success(decoded))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp


def follow(request):
    try:
        action = 'follow'

        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        assert_dir(decoded, 'request')
        assert_content_type(decoded, 'account')
        assert_account_action(decoded, 'follow')

        json_content_data = decoded['content']['data']
        if 'person' not in json_content_data:
            raise BadJSONType

        # search database and compare password
        user = UserAccount.login(decoded['signature'])
        follow_user = UserAccount.objects.get(email=json_content_data['person'])

        if UserFollow.objects.filter(user=user, follow_user=follow_user).exists():
            raise AlreadyFollow

        follow_relation = UserFollow(
            user=user,
            follow_user=follow_user
        )
        follow_relation.save()

    # wrong password
    except LoginFail:
        http_resp = HttpResponse(gen_follow_response(action, STATUS_LOGIN_FAIL))

    except AlreadyFollow:
        http_resp = HttpResponse(gen_follow_response(action, STATUS_ALREADY_FOLLOW))

    # bad JSON format
    except (json.JSONDecodeError, KeyError, BadJSONType):
        http_resp = HttpResponse(gen_follow_response(action, STATUS_CORRUPTED_JSON))

    except UserAccount.DoesNotExist:
        http_resp = HttpResponse(gen_follow_response(action, STATUS_NO_SUCH_PERSON))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_follow_response(action, STATUS_OTHER_FAILURE))

    # success
    else:
        http_resp = HttpResponse(gen_follow_response(action, STATUS_SUCCESS))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp


def unfollow(request):
    try:
        action = 'unfollow'

        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # check the type of JSON query
        assert_dir(decoded, 'request')
        assert_content_type(decoded, 'account')
        assert_account_action(decoded, 'unfollow')

        json_content_data = decoded['content']['data']
        if 'person' not in json_content_data:
            raise BadJSONType

        # search database and compare password
        user = UserAccount.login(decoded['signature'])
        follow_user = UserAccount.objects.get(email=json_content_data['person'])

        if not UserFollow.objects.filter(user=user, follow_user=follow_user).exists:
            raise AlreadyUnfollow

        follow_relation = UserFollow.objects.filter(user=user, follow_user=follow_user)
        follow_relation.delete()

    # wrong password
    except LoginFail:
        http_resp = HttpResponse(gen_follow_response(action, STATUS_LOGIN_FAIL))

    except AlreadyUnfollow:
        http_resp = HttpResponse(gen_follow_response(action, STATUS_ALREADY_UNFOLLOW))

    # bad JSON format
    except (json.JSONDecodeError, KeyError, BadJSONType):
        http_resp = HttpResponse(gen_follow_response(action, STATUS_CORRUPTED_JSON))

    except UserAccount.DoesNotExist:
        http_resp = HttpResponse(gen_follow_response(action, STATUS_NO_SUCH_PERSON))

    # other unknown exceptions
    except Exception as e:
        print(e)
        http_resp = HttpResponse(gen_follow_response(action, STATUS_OTHER_FAILURE))

    # success
    else:
        http_resp = HttpResponse(gen_follow_response(action, STATUS_SUCCESS))

    http_resp["Access-Control-Allow-Origin"] = "*"
    return http_resp
