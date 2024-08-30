from django.shortcuts import render, redirect
from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm


def user_list(request):
    """ User Management """

    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=2)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """ Add User (Original Method) """

    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    # Retrieve data submitted by the user
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # Add to the database
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=account, create_time=ctime,
                                   gender=gender, depart_id=depart_id)

    # Redirect to user list page
    return redirect("/user/list/")


def user_model_form_add(request):
    """ Add User (ModelForm Version) """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # User submits data via POST, data validation
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # If the data is valid, save to the database
        # {'name': '123', 'password': '123', 'age': 11, 'account': Decimal('0'), 'create_time': datetime.datetime(2011, 11, 11, 0, 0, tzinfo=<UTC>), 'gender': 1, 'depart': <Department: IT Department>}
        # print(form.cleaned_data)
        # models.UserInfo.objects.create(..)
        form.save()
        return redirect('/user/list/')

    # Validation failed (display error message on the page)
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """ Edit User """
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # Fetch the row of data to be edited from the database by ID (object)
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # By default, all data entered by the user is saved; if you want to add a value beyond the user's input
        # form.instance.field_name = value
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    """ Delete User """
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

