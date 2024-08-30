from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """ Data Statistics Page """
    return render(request, 'chart_list.html')


def chart_bar(request):
    """ Construct data for the bar chart """
    # Data can be fetched from the database
    legend = ["Liang Jining", "Wu Peiqi"]
    series_list = [
        {
            "name": 'Liang Jining',
            "type": 'bar',
            "data": [15, 20, 36, 10, 10, 10]
        },
        {
            "name": 'Wu Peiqi',
            "type": 'bar',
            "data": [45, 10, 66, 40, 20, 50]
        }
    ]
    x_axis = ['Jan', 'Feb', 'Apr', 'May', 'Jun', 'Jul']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """ Construct data for the pie chart """

    db_data_list = [
        {"value": 2048, "name": 'IT Department'},
        {"value": 1735, "name": 'Operations'},
        {"value": 580, "name": 'New Media'},
    ]

    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    """ Construct data for the line chart """
    legend = ["Shanghai", "Guangxi"]
    series_list = [
        {
            "name": 'Shanghai',
            "type": 'line',
            "stack": 'Total',
            "data": [15, 20, 36, 10, 10, 10]
        },
        {
            "name": 'Guangxi',
            "type": 'line',
            "stack": 'Total',
            "data": [45, 10, 66, 40, 20, 50]
        }
    ]
    x_axis = ['Jan', 'Feb', 'Apr', 'May', 'Jun', 'Jul']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def highcharts(request):
    """ Highcharts example """
    return render(request, 'highcharts.html')


from django.forms import ModelForm
from app01 import models


# class TTModelForm(Form):
#     name = forms.CharField(label="Username")
#     ff = forms.FileField(label="File")
#
#
# def tt(request):
#     if request.method == "GET":
#         form = TTModelForm()
#         return render(request, 'change.html', {"form": form})
#     form = TTModelForm(data=request.POST, files=request.FILES)
#     if form.is_valid():
#         print(form.cleaned_data)
#     return render(request, 'change.html', {"form": form})

class TTModelForm(ModelForm):
    class Meta:
        model = models.XX
        fields = "__all__"


def tt(request):
    """ Example view for form handling """
    instance = models.XX.objects.all().first()
    if request.method == "GET":
        form = TTModelForm(instance=instance)
        return render(request, 'tt.html', {"form": form})
    form = TTModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
    return render(request, 'tt.html', {"form": form})

