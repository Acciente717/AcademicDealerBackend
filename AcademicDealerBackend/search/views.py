from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from users.models import UserAccount, LoginFail
from Project.models import ProjectInfo, ProjectMember, ProjectComment
from seminar.models import SeminarInfo, SeminarComment, SeminarMember
from lab.models import LabInfo, LabComment
from django.utils import timezone
import json

STATUS_SUCCESS = 0
STATUS_OTHER_ERROR = 1
STATUS_CORRUPTED_JSON = 2

class BadJSONType(RuntimeError):
    pass

def search_owned_something(info_class, keywords, owner_email,
                           search_description, search_outdated):

    ### search title
    keywords = keywords.split(' ')
    title_result = info_class.objects.all()

    # apply owner_email restriction
    if owner_email:
        title_result = title_result.filter(owner__email=owner_email)

    # apply keyword restriction
    for keyword in keywords:
        title_result = title_result.filter(name__contains=keyword)

    # exclude outdated if required
    if not search_outdated:
        title_result = title_result.filter(end_date__gte=timezone.now())

    ### search the description of projcet if needed
    if search_description:

        # apply owner_email restriction
        description_result = info_class.objects.all()
        if owner_email:
            description_result = description_result.filter(owner__email=owner_email)

        # apply keyword restriction
        for keyword in keywords:
            description_result = description_result.filter(description__contains=keyword)

        # exclude outdated if required
        if not search_outdated:
            description_result = description_result.filter(end_date__gte=timezone.now())

        # union with previous result
        title_result = title_result.union(description_result)

    lst = [ {"content_type" : "project",
             "id" : i.id,
             "date" : timezone.localtime(i.modified_date) } for i in title_result]
    return lst

def search_attended_something(member_class, keywords, attender_email,
                              search_description, search_outdated):

    ### search title
    keywords = keywords.split(' ')
    title_result = member_class.objects.all()

    # apply attender email restriction
    if attender_email:
        title_result = title_result.filter(person__email=attender_email)

    # apply keyword restriction
    for keyword in keywords:
        title_result = title_result.filter(project__name__contains=keyword)

    # exclude outdated if required
    if not search_outdated:
        title_result = title_result.filter(project__end_date__gte=timezone.now())

    ### search the description of projcet if needed
    if search_description:

        # apply owner_email restriction
        description_result = member_class.objects.all()
        if attender_email:
            description_result = description_result.filter(person__email=attender_email)

        # apply keyword restriction
        for keyword in keywords:
            description_result = description_result.filter(project__description__contains=keyword)

        # exclude outdated if required
        if not search_outdated:
            description_result = description_result.filter(project__end_date__gte=timezone.now())

        # union with previous result
        title_result = title_result.union(description_result)

    lst = [ {"content_type" : "project",
              "id" : i.project.id,
              "date" : timezone.localtime(i.project.modified_date) } for i in title_result]
    return lst

def build_search_result(total_results, total_page_num, result_list):
    dic = {
    "dir": "response",
    "content_type": "search",
    "status": STATUS_SUCCESS,
    "content": {
        "total_results" : total_results,
        "last_page": total_page_num,
        "result": result_list
    }
}
    return json.dumps(dic)

def build_search_error(error_code):
    dic = {
    "dir": "response",
    "content_type": "search",
    "status": error_code,
    "content": {}
}
    return json.dumps(dic)

def api(request):

    try:
        body = str(request.body, encoding='utf8')
        decoded = json.loads(body)

        if decoded['dir'] != 'request' or decoded['content_type'] != 'search':
            raise BadJSONType

        json_content_data = decoded['content']
        keywords = json_content_data['keyword']
        email = json_content_data['user_email']
        search_seminar = json_content_data["search_seminar"]
        search_project = json_content_data["search_project"]
        search_lab = json_content_data["search_lab"]
        search_outdated = json_content_data['search_outdated']
        search_description = json_content_data['search_description']
        request_page = json_content_data['curr_page']

        if json_content_data['user_type'] == 'owner':

            # search for owned projects
            projects = search_owned_something(ProjectInfo, keywords, email,
                                            search_description, search_outdated)\
                if search_project else []

            # search for owned labs
            labs = search_owned_something(LabInfo, keywords, email,
                                        search_description, search_outdated)\
                if search_lab else []

            # search for seminars
            seminars = search_owned_something(SeminarInfo, keywords, email,
                                            search_description, search_outdated)\
                if search_seminar else []


        elif json_content_data['user_type'] == 'attender':

            # search for attended projects
            projects = search_attended_something(ProjectMember, keywords, email,
                                                search_description, search_outdated)\
                if search_project else []

            # no lab can be attended
            labs = []

            # search for attended seminars
            seminars = search_attended_something(SeminarMember, keywords, email,
                                                search_description, search_outdated)\
                if search_seminar else []
        else:
            raise BadJSONType

        # build response
        full_list = projects + labs + seminars
        full_list.sort(key=lambda x : x['date'], reverse=True)
        full_list = [ { "content_type" : i['content_type'],
                        "id" : i['id'] }
                    for i in full_list[request_page * 10 : (request_page + 1) * 10] ]
        resp = build_search_result(len(full_list), len(full_list) // 10,
                                full_list)
        http_resp = HttpResponse(resp)

    # bad JSON structure or missing field
    except (json.JSONDecodeError, BadJSONType, KeyError):
        http_resp = HttpResponse(build_search_error(STATUS_CORRUPTED_JSON))

    # unknown exception
    except Exception as e:
        print('Error: unknown exception occured at search!')
        print(e)
        http_resp = HttpResponse(build_search_error(STATUS_OTHER_ERROR))

    return http_resp
