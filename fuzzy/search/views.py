from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import logging
from .models import WordBank


def index(request, template_name='search.html'):
    return render(request, template_name)

def configure(request, template_name='configure.html'):
    return render(request, template_name)

def RecieveFiles(request):
    data={}
    return JsonResponse(data)


def upload_csv(request):
    data={};
    data['result']="success"

    if "GET" == request.method:

        return render(request, "search.html", data)

    try:

        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.tsv'):
            messages.error(request,'File is not TSV type')
            return HttpResponseRedirect(reverse("upload_csv"))
        # if csv_file.multiple_chunks():
        #     print("Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000)))
        #     messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        #     return HttpResponseRedirect(reverse("upload_csv"))

        file_data = csv_file.read().decode("utf-8")


        lines = file_data.split("\n")
        # print(lines)
        #loop over the lines and save them in db. If error , store as string and then display
        dataf=[]
        for line in lines:
            fields = line.split("\t")
            if(fields[0]!=''):
                data_dict = {}
                data_dict["word"] = fields[0]
                data_dict["frequency"] = fields[1]
            # print(data_dict)
                dataf.append(WordBank(word=fields[0],frequency=fields[1]))
        # print(dataf)
        WordBank.objects.bulk_create(dataf)
            # try:
            #     form = WordBank(word=fields[0],frequency=fields[1])
            #     form.save()
            # except Exception as e:
            #     logging.getLogger("error_logger").error(repr(e))
            #     pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("upload_csv"))

def autocomplete(request):
    data={}
    if request.method == "GET":

        search_qs = WordBank.objects.filter(word__startswith=request.GET.get('search', None))[:20]
        results = []
        for r in search_qs:
            results.append(r.word)

        return JsonResponse(results,safe=False)

    data['error']="Not Ajax"
    return JsonResponse(data)
