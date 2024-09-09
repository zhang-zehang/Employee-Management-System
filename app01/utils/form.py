from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from app01.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["username", "password", "age", 'account', 'create_time', "gender", "depart"]


class PrettyModelForm(BootStrapModelForm):
    # Validation: Method 1
    mobile = forms.CharField(
        label="Mobile Number",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', 'Invalid mobile number format'), ],
    )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        # exclude = ['level']
        fields = ["mobile", 'price', 'level', 'status']

    # Validation: Method 2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("Mobile number already exists")

        # Validation passed, return the user's input
        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="Mobile Number")
    mobile = forms.CharField(
        label="Mobile Number",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', 'Invalid mobile number format'), ],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    # Validation: Method 2
    def clean_mobile(self):
        # ID of the current row being edited
        # print(self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("Mobile number already exists")

        # Validation passed, return the user's input
        return txt_mobile
    

from django import forms
from app01.models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # 使用 HTML5 日期选择器
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # 使用 HTML5 日期选择器
        label="End Date"
    )

    class Meta:
        model = LeaveRequest
        fields = ['reason', 'start_date', 'end_date']  # 添加开始和结束时间


