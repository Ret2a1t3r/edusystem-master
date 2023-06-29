import re

from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from django.shortcuts import render, redirect

from school import models
from school.utils import pagination, bootstrap
from school.views.create import create_teach_id
from django.contrib.auth.decorators import login_required
from teacher_Interface import IEditTeachService, IDeleteTeachService, IAddTeachService, IShowTeachInfoService
from teacher import TeachForm


class ShowTeachInfoService(IShowTeachInfoService):
    def __init__(self, request):
        self.request = request

    def show_teach_info(self):
        value = self.request.GET.get('value', '')
        data_dict = {}
        if value:
            if value.isdigit():
                data_dict['user__username__contains'] = value
            else:
                data_dict['name__contains'] = value
        teachers = models.Teacher.objects.filter(**data_dict).order_by('user__username')

        page_obj = pagination.Pagination(self.request, teachers)

        context = {
            'value': value,

            'teachers': page_obj.page_queryset,
            'page_string': page_obj.html()
        }

        return render(self.request, 'teacher_list.html', context)


class AddTeachService(IAddTeachService):
    def __init__(self, request):
        self.request = request

    def teach_add(self):
        if self.request.method == "GET":
            teach_form = TeachForm()
            return render(self.request, 'teacher_add.html', {'teachForm': teach_form})
        else:
            form = TeachForm(self.request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                gender = form.cleaned_data.get('gender')
                born_date = form.cleaned_data.get('born_date')
                entry_date = form.cleaned_data.get('entry_date')
                department_name = form.cleaned_data.get('department_name')
                title = form.cleaned_data.get('title')

                teach_id = create_teach_id()
                models.User.objects.create(username=teach_id, password='123456', identify=2)
                user = models.User.objects.filter(username=teach_id).first()
                models.Teacher.objects.create(user=user, name=name, gender=gender, born_date=born_date,
                                              entry_date=entry_date, department_name=department_name,
                                              title=title)
                return redirect('/teach/list')
            else:
                return render(self.request, 'teacher_add.html', {'teachForm': form})


class DeleteTeachService(IDeleteTeachService):
    def __init__(self, request):
        self.request = request

    def teach_delete(self):
        teach_id = self.request.GET.get('uid')
        models.User.objects.filter(username=teach_id).delete()
        return JsonResponse({
            'status': True,
        })


class EditTeachService(IEditTeachService):
    def __init__(self, request):
        self.request = request

    def teach_edit(self, teach_id):
        if self.request.method == 'GET':
            row_object = models.Teacher.objects.filter(user__username=teach_id).values('name', 'gender', 'born_date',
                                                                                       'entry_date', 'title',
                                                                                       'department_name').first()

            teach_form = TeachForm(initial=row_object)
            return render(self.request, 'teacher_edit.html', {'teachForm': teach_form})

        else:
            form = TeachForm(self.request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                gender = form.cleaned_data.get('gender')
                born_date = form.cleaned_data.get('born_date')
                entry_date = form.cleaned_data.get('entry_date')
                department_name = form.cleaned_data.get('department_name')
                title = form.cleaned_data.get('title')

                models.Teacher.objects.filter(user__username=teach_id).update(name=name, gender=gender,
                                                                              born_date=born_date,
                                                                              entry_date=entry_date,
                                                                              department_name=department_name,
                                                                              title=title)
                return redirect('/teach/list/')
        return render(request, 'teacher_edit.html', {'form': form})