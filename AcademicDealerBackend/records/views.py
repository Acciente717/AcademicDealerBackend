from django.shortcuts import render
from .models import Records
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse



# Create your views here.

def detail(request):
    records_list = Records.objects.all()
    template = loader.get_template('records/records.html')
    context = {
        'records_list': records_list,
    }
    return HttpResponse(template.render(context, request))

def insert(request):
    try:
        input_str = request.POST['input_str']
    except (KeyError):
        # Redisplay the question voting form.
        return render(request, 'records/records.html', {
            'error_message': "Empty input.",
        })
    else:
        record = Records(record_text=input_str)
        record.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('records:detail'))

def delete(request):
    for k, v in request.POST.items():
        if '__record_id' in k and v == 'on':
            pk = k.split('.')[1]
            record = Records.objects.get(pk=pk)
            record.delete()
        print("k =", k, "v = ", v)
    return HttpResponseRedirect(reverse('records:detail'))