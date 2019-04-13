from django.http import HttpResponse, HttpRequest

# Create your views here.

def index(request):
    # print(request.body)
    return HttpResponse(request.body)


