from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.decorators import user_passes_test
from app01.models import LeaveRequest
from app01.utils.form import LeaveRequestForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def is_manager(request):
    return request.session.get("info") and request.session["info"].get("role") == 1
@csrf_exempt
def leave_request_create(request):
    if "info" not in request.session:
        return redirect('/login/')
    
    # Check if the user is an employee
    if request.session['info']['role'] != 2:
        return HttpResponse("Unauthorized", status=403)
    
    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            # Set the employee to the current session user
            leave_request.employee_id = request.session["info"]["id"]
            leave_request.save()
            return redirect('my_leave_requests')  # 跳转到员工的请假申请列表页面
    else:
        form = LeaveRequestForm()

    return render(request, 'leave_request_create.html', {'form': form})




'''@csrf_exempt
def leave_request_list(request):
    # Check if the user is logged in
    if "info" not in request.session:
        return redirect('/login/')
    
    # Check if the user is a manager
    if request.session['info']['role'] != 1:
        return HttpResponse("Unauthorized", status=403)

    requests = LeaveRequest.objects.filter(status=1)  # 只显示待审批的申请
    return render(request, 'leave_request_list.html', {'requests': requests})'''

@csrf_exempt
def leave_request_list(request):
    # 检查用户是否为管理员
    if request.session.get("info", {}).get("role") != 1:
        return HttpResponse("Unauthorized", status=403)

    # 获取所有员工的请假申请
    leave_requests = LeaveRequest.objects.all().order_by('-created_at')

    # 渲染模板并传递数据
    leave_requests = LeaveRequest.objects.filter(status=1)
    return render(request, 'leave_request_list.html', {'leave_requests': leave_requests})

@csrf_exempt
def leave_request_approve(request, pk):
    # 检查用户是否登录以及是否为管理员
    if not is_manager(request):
        return HttpResponse("Unauthorized", status=403)

    leave_request = LeaveRequest.objects.get(id=pk)
    leave_request.status = 2  # Approved
    leave_request.save()
    return redirect('leave_request_list')

@csrf_exempt
def leave_request_reject(request, pk):
    # 检查用户是否登录以及是否为管理员
    if not is_manager(request):
        return HttpResponse("Unauthorized", status=403)

    leave_request = LeaveRequest.objects.get(id=pk)
    leave_request.status = 3  # Rejected
    leave_request.save()
    return redirect('leave_request_list')

@csrf_exempt
def my_leave_requests(request):
    # 检查用户是否登录
    if "info" not in request.session:
        return redirect('/login/')
    
    # 获取当前员工的 ID
    employee_id = request.session["info"]["id"]
    
    # 获取该员工的所有请假申请记录
    leave_requests = LeaveRequest.objects.filter(employee_id=employee_id).order_by('-created_at')
    
    # 渲染模板并传递数据
    return render(request, 'my_leave_requests.html', {'leave_requests': leave_requests})

