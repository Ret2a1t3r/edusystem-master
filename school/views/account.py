from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django import forms
from school.utils import bootstrap
from school import models


class LoginForm(bootstrap.BootStrapForm):
    username = forms.CharField(label='用户名', widget=forms.TextInput, required=True)
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True), required=True)


def sign_in(request):
    if request.user.is_authenticated:
        identify = request.user.identify
        if identify == 1:
            return redirect('/stu/list/')
        elif identify == 2:
            return redirect('/course/list2/')
        else:
            return redirect('/course/list3/')
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if not user:
                form.add_error('password', '用户名或密码错误')
                return render(request, 'login.html', {'form': form})
            login(request, user)
            if user.identify == 1:  # 教务人员
                request.session['name'] = models.Teacher.objects.filter(user__username=username).first().name
                return redirect('/stu/list/')
            elif user.identify == 2:  # 教师
                request.session['name'] = models.Teacher.objects.filter(user__username=username).first().name
                return redirect('/course/list2/')
            else:  # 学生
                request.session['name'] = models.Student.objects.filter(user__username=username).first().name
                return redirect('/course/list3/')

        else:
            return render(request, 'login.html', {'form': form})


def sign_out(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
    return redirect('/login/')


def get_modify_pwd_page(request):
    identify = request.user.identify
    if identify == 1:
        return render(request, 'manager_modify_pwd.html')
    elif identify == 2:
        return render(request, 'teacher_modify_pwd.html')
    else:
        return render(request, 'student_modify_pwd.html')


def modify_password(request):
    now_password = request.GET.get('now_password')
    if not request.user.check_password(now_password):
        return JsonResponse({
            'status': False,
        })
    new_password = request.GET.get('new_password')
    request.user.set_password(new_password)
    request.user.save()
    return JsonResponse({
        'status': True,
    })
