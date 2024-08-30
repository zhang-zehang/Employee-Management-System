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
    """ Login """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # Validation successful, retrieve the username and password
        # {'username': 'wupeiqi', 'password': '123',"code":123}
        # {'username': 'wupeiqi', 'password': '5e5c3bad7eb35cba3638e145c830c35f',"code":xxx}

        # Verification code validation
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "Verification code error")
            return render(request, 'login.html', {'form': form})

        # Check in the database if the username and password are correct, get user object or None
        # admin_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "Username or password incorrect")
            # form.add_error("username", "Username or password incorrect")
            return render(request, 'login.html', {'form': form})

        # Username and password are correct
        # The website generates a random string; writes it into the user's browser cookie; and writes it into the session;
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        # Session can be saved for 7 days
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/admin/list/")

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

