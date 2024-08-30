from django.shortcuts import render, redirect
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


def city_list(request):
    """ View to display list of cities """
    queryset = models.City.objects.all()
    return render(request, 'city_list.html', {'queryset': queryset})


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = "__all__"


def city_add(request):
    """ Add new city """
    title = "Add New City"

    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # For files: automatically save;
        # Fields + upload path written to the database
        form.save()
        return redirect("/city/list/")
    return render(request, 'upload_form.html', {"form": form, 'title': title})

