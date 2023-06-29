from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse

import re
from django.shortcuts import render, redirect

from django.db.models import Q
from school import models
from school.utils import pagination, bootstrap
from school.views.create import create_stu_id
from django.contrib.auth.decorators import login_required

from student_implement import AddStudentService, DeleteStudentService, EditStudentService, ShowStuInfoService, \
    ShowStuClassInfoService, ShowStuInPreviousClassService, QueryGradeService


class StuForm(bootstrap.BootStrapForm):
    gender_choice = (
        (1, "男"),
        (2, "女")
    )

    name = forms.CharField(label='姓名')
    gender = forms.ChoiceField(label='性别', choices=gender_choice, widget=forms.Select)
    born_date = forms.DateField(label="出生日期")
    enrollment_date = forms.DateField(label="入学日期")
    department_name = forms.CharField(label="系")
    major_name = forms.CharField(label="专业")
    class_name = forms.CharField(label="班级")

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

    def clean_major_name(self):
        major_name = self.cleaned_data['major_name']
        if not models.Student.objects.filter(major_name=major_name):
            raise ValidationError('输入的专业不存在。')
        return major_name

    def clean_class_name(self):
        class_name = self.cleaned_data['class_name']
        if not models.Student.objects.filter(class_name=class_name):
            raise ValidationError('输入的班级不存在。')
        return class_name


class AddStudent:
    def __init__(self, cls):
        self.cls = cls

    def student_add(self):
        return self.cls.student_add()


class DeleteStudent:
    def __init__(self, cls):
        self.cls = cls

    def student_delete(self):
        return self.cls.student_delete()


class EditStudent:
    def __init__(self, cls):
        self.cls = cls

    def student_edit(self, stu_id):
        return self.cls.student_edit(stu_id)


class ShowStudentInfo:
    def __init__(self, cls):
        self.cls = cls

    def show_student_info(self):
        self.cls.show_student_info()


class ShowStuClassInfo:
    def __init__(self, cls):
        self.cls = cls

    def show_stu_in_class_info(self, tp_id):
        self.cls.show_stu_in_class_info(tp_id)


class ShowStuInPreviousClass:
    def __init__(self, cls):
        self.cls = cls

    def show_stu_in_previous_class_info(self, tp_id):
        self.cls.show_stu_in_previous_class_info(tp_id)

class QueryGrade:
    def __init__(self, cls):
        self.cls = cls

    def query_grade(self):
        self.cls.query_grade()


@login_required
def stu_list(request):
    show_stu_info_service = ShowStuInfoService(request)
    drive = ShowStudentInfo(show_stu_info_service)
    return drive.show_student_info()


@login_required
def stu_add(request):
    stu_add_service = AddStudentService(request)
    drive = AddStudent(stu_add_service)
    return drive.student_add()


@login_required
def stu_delete(request):
    stu_delete_service = DeleteStudentService(request)
    drive = DeleteStudent(stu_delete_service)
    return drive.student_delete()


@login_required
def stu_edit(request, stu_id):
    stu_edit_service = EditStudentService(request)
    drive = EditStudent(stu_edit_service)
    return drive.student_edit(stu_id)


def stu_in_class_list(request, tp_id):
    show_stu_class_info_service = ShowStuClassInfoService(request)
    drive = ShowStuClassInfoService(show_stu_class_info_service)
    return drive.show_stu_in_class_info(tp_id)


def stu_in_previous_class_list(request, tp_id):
    show_stu_in_previous_class_service = ShowStuInPreviousClassService(request)
    drive = ShowStuInPreviousClass(show_stu_in_previous_class_service)
    return drive.show_stu_in_previous_class_info(tp_id)


def query_grade(request):
    query_grade_service = QueryGradeService(request)
    drive = QueryGrade(query_grade_service)
    return drive.query_grade()