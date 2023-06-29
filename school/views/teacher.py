import re

from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from django.shortcuts import render, redirect

from school import models
from school.utils import pagination, bootstrap
from school.views.create import create_teach_id
from django.contrib.auth.decorators import login_required
from teacher_Interface import IDeleteTeachService, IEditTeachService, IShowTeachInfoService, IAddTeachService
from teacher_implement import ShowTeachInfoService, EditTeachService, DeleteTeachService, AddTeachService


class TeachForm(bootstrap.BootStrapForm):
    gender_choice = (
        (1, "男"),
        (2, "女")
    )

    title_choice = (
        (1, "助教"),
        (2, "讲师"),
        (3, "副教授"),
        (4, "教授"),
    )

    name = forms.CharField(label='姓名')
    gender = forms.ChoiceField(label='性别', choices=gender_choice, widget=forms.Select)
    born_date = forms.DateField(label="出生日期")
    entry_date = forms.DateField(label="入职日期")
    title = forms.ChoiceField(label="职称", choices=title_choice, widget=forms.Select)
    department_name = forms.CharField(label="系")

    def clean_name(self):
        chinese = re.compile(r'^[\u4e00-\u9fa5]{2,8}$')
        name = self.cleaned_data['name']
        if not chinese.findall(name):
            raise ValidationError('请输入2-8个汉字。')
        return name

    def clean_department_name(self):
        department_name = self.cleaned_data['department_name']
        if not models.Student.objects.filter(department_name=department_name):
            raise ValidationError('输入的系不存在。')
        return department_name


class ShowTeachInfo:
    def __init__(self, cls):
        self.cls = cls

    def show_teach_info(self):
        self.cls.show_teach_info()


class AddTeach:
    def __init__(self, cls):
        self.cls = cls

    def teach_add(self):
        self.cls.teach_add()


class DeleteTeach:
    def __init__(self, cls):
        self.cls = cls

    def teach_delete(self):
        self.cls.teach_delete()


class EditTeach:
    def __init__(self, cls):
        self.cls = cls

    def teach_edit(self, teach_id):
        self.cls.teach_edit(teach_id)


@login_required
def teach_list(request):
    show_teach_info_service = ShowTeachInfoService(request)
    drive = ShowTeachInfo(show_teach_info_service)
    return drive.show_teach_info()


@login_required
def teach_add(request):
    teach_add_service = AddTeachService(request)
    drive = AddTeach(teach_add_service)
    return drive.teach_add()


@login_required
def teach_delete(request):
    teach_delete_service = DeleteTeachService(request)
    drive = DeleteTeach(teach_delete_service)
    return drive.teach_delete()


@login_required
def teach_edit(request, teach_id):
    teach_edit_service = EditTeachService(request)
    drive = EditTeach(teach_edit_service)
    return drive.teach_edit(teach_id)
