from django.shortcuts import render
from .models import UserAccount
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import json
from .utils import *

def register(request):
    try:
        # decode http content to JSON
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        # sanity check
        assert_dir(decoded, 'request')
        assert_content_type(decoded, 'account')
        assert_account_action(decoded, "register")

        # create new user
        json_signature = decoded['signature']
        json_content_data = decoded['content']['data']
        new_user = UserAccount(
            email = json_signature['user_email'],
            pw_hash = json_signature['password_hash'],
            real_name = json_content_data['real_name'],
            nick_name = json_content_data['nick_name'],
            pic_url = json_content_data['pic_url'],
            school = json_content_data['school'],
            department = json_content_data['department'],
            title = json_content_data['title'],
            enrollment_date = json_content_data['enrollment_date'],
            profile = json_content_data['profile']
        )
        new_user.save()
    
    # bad JSON format
    except json.JSONDecodeError:
        return HttpResponse(gen_register_fail(None, REGISTER_INVALID_JSON))
    
    # duplicated email or nickname
    except IntegrityError:
        return HttpResponse(gen_register_fail(decoded, REGISTER_DUPLICATE_MAIL_NICKNAME))
    
    # wrong format of specific fields
    # for example, date must be in "yyyy-mm-dd"
    except ValidationError:
        return HttpResponse(gen_register_fail(decoded, REGISTER_INVALID_FIELD))
    
    # other unknown exceptions
    except Exception:
        return HttpResponse(gen_register_fail(decoded, REGISTER_OTHER_ERROR))
    
    # success
    return HttpResponse(gen_register_success(decoded))
    
