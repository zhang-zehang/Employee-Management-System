import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea,
            "detail": forms.TextInput
        }


def task_list(request):
    """ Task List """
    # Retrieve all tasks from the database
    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)

    form = TaskModelForm()

    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # Paginated data
        "page_string": page_object.html()  # Pagination HTML
    }
    return render(request, "task_list.html", context)


@csrf_exempt
def task_ajax(request):
    """ Handle AJAX requests for tasks """
    print(request.GET)
    print(request.POST)

    data_dict = {"status": True, 'data': [11, 22, 33, 44]}
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    """ Add Task (AJAX Request) """
    # {'level': ['1'], 'title': ['sdfsdfsdfsd'], 'detail': ['111'], 'user': ['8']}
    # print(request.POST)

    # 1. Validate data sent by the user (ModelForm validation)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

