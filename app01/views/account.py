from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO

from app01.utils.code import check_code
from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="Verification Code",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "Verification code error")
            return render(request, 'login.html', {'form': form})

        # Check username and password in Admin
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if admin_object:
            # Role-based redirection
            request.session["info"] = {'id': admin_object.id, 'name': admin_object.username, 'role': admin_object.role}
            request.session.set_expiry(60 * 60 * 24 * 7)
            
            if admin_object.role == 1:  # Manager
                return redirect("/admin/list/")  # 跳转到管理员界面
            else:
                return redirect("/task/list/")  # 跳转到员工的任务管理页面

        form.add_error("password", "Username or password is incorrect")
        return render(request, 'login.html', {'form': form})

    return render(request, 'login.html', {'form': form})



def image_code(request):
    """ Generate image verification code """

    # Call pillow function to generate an image
    img, code_string = check_code()

    # Write into session (for subsequent verification)
    request.session['image_code'] = code_string
    # Set Session timeout to 60s
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ Logout """

    request.session.clear()

    return redirect('/login/')

