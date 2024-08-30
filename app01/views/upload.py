import os
from django.conf import settings
from django.shortcuts import render, HttpResponse
from app01 import models


def upload_list(request):
    """ View for file upload list """
    if request.method == "GET":
        return render(request, 'upload_list.html')

    # # 'username': ['big666']
    # print(request.POST)  # Data in the request body
    # # {'avatar': [<InMemoryUploadedFile: image1.png (image/png)>]}
    # print(request.FILES)  # Files sent in the request {}

    file_object = request.FILES.get("avatar")
    # print(file_object.name)  # File name: WX20211117-222041@2x.png

    with open(file_object.name, mode='wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)

    return HttpResponse("...")


from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(label="Name")
    age = forms.IntegerField(label="Age")
    img = forms.FileField(label="Avatar")


def upload_form(request):
    """ Form upload """
    title = "Form Upload"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # {'name': 'Wu Peiqi', 'age': 123, 'img': <InMemoryUploadedFile: image1.png (image/png)>}
        # 1. Read image content, write to folder, and get the file path.
        image_object = form.cleaned_data.get("img")

        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
        media_path = os.path.join("media", image_object.name)
        with open(media_path, mode='wb') as f:
            for chunk in image_object.chunks():
                f.write(chunk)

        # 2. Write the image file path to the database
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )
        return HttpResponse("...")
    return render(request, 'upload_form.html', {"form": form, "title": title})


from django import forms
from app01.utils.bootstrap import BootStrapModelForm


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = "__all__"


def upload_modal_form(request):
    """ Upload file and data (ModelForm) """
    title = "ModelForm Upload File"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # For files: automatically save;
        # Fields + upload path written to the database
        form.save()

        return HttpResponse("Success")
    return render(request, 'upload_form.html', {"form": form, 'title': title})

