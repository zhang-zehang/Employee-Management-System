"""day16 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from app01.views import depart, user, pretty, admin, account, task, order, chart, upload, city,leave,gradio

urlpatterns = [
    # path('admin/', admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    path('tt/', chart.tt),

    # Department Management
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),
    path('depart/multi/', depart.depart_multi),

    # User Management
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/model/form/add/', user.user_model_form_add),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    # Pretty Number Management
    path('pretty/list/', pretty.pretty_list),
    path('pretty/add/', pretty.pretty_add),
    path('pretty/<int:nid>/edit/', pretty.pretty_edit),
    path('pretty/<int:nid>/delete/', pretty.pretty_delete),

    # Admin Management
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # Login
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # Task Management
    path('task/list/', task.task_list),
    path('task/ajax/', task.task_ajax),  # Learn Ajax
    path('task/add/', task.task_add),

    # Order Management
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # Data Statistics
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),
    path('chart/highcharts/', chart.highcharts),

    # File Upload
    path('upload/list/', upload.upload_list),
    path('upload/form/', upload.upload_form),
    path('upload/modal/form/', upload.upload_modal_form),

    # City List
    path('city/list/', city.city_list),
    path('city/add/', city.city_add),

    path('leave/request/', leave.leave_request_create, name='leave_request_create'),
    path('leave/requests/', leave.leave_request_list, name='leave_request_list'),
    path('leave/my_requests/', leave.my_leave_requests, name='my_leave_requests'),
    path('leave/request/approve/<int:pk>/', leave.leave_request_approve, name='leave_request_approve'),
    path('leave/request/reject/<int:pk>/', leave.leave_request_reject, name='leave_request_reject'),

    path('embed_gradio/', gradio.embed_gradio_view, name='embed_gradio'),
]

