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
from student_Interface import IAddStudentService, IEditStudentService, IDeleteStudentService, IShowStuInfoService, \
    IShowStuInClassInfoService, IShowStuInPreviousClassService, IQueryGradeService
from student import StuForm


class AddStudentService(IAddStudentService):
    def __init__(self, request):
        self.request = request

    def stu_add(self):
        if self.request.method == "GET":
            stu_form = StuForm()
            return render(self.request, 'student_add.html', {'stuForm': stu_form})
        else:
            form = StuForm(self.request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                gender = form.cleaned_data.get('gender')
                born_date = form.cleaned_data.get('born_date')
                enrollment_date = form.cleaned_data.get('enrollment_date')
                department_name = form.cleaned_data.get('department_name')
                major_name = form.cleaned_data.get('major_name')
                class_name = form.cleaned_data.get('class_name')

                stu_id = create_stu_id(class_name[0] + class_name[1])
                models.User.objects.create(username=stu_id, password='123456', identify=3)
                user = models.User.objects.filter(username=stu_id).first()
                models.Student.objects.create(user=user, name=name, gender=gender, born_date=born_date,
                                              enrollment_date=enrollment_date, department_name=department_name,
                                              major_name=major_name, class_name=class_name)
                return redirect('/stu/list')
            else:
                return render(self.request, 'student_add.html', {'stuForm': form})


class DeleteStudentService(IDeleteStudentService):
    def __init__(self, request):
        self.request = request

    def stu_delete(self):
        stu_id = self.request.GET.get('uid')
        models.User.objects.filter(username=stu_id).delete()
        return JsonResponse({
            'status': True,
        })


class EditStudentService(IEditStudentService):
    def __init__(self, request):
        self.request = request

    def stu_edit(self, stu_id):
        if self.request.method == 'GET':
            row_object = models.Student.objects.filter(user__username=stu_id).values('name', 'gender', 'born_date',
                                                                                     'enrollment_date',
                                                                                     'department_name',
                                                                                     'major_name', 'class_name').first()

            stu_form = StuForm(initial=row_object)
            return render(self.request, 'student_edit.html', {'stuForm': stu_form})

        else:
            form = StuForm(self.request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                gender = form.cleaned_data.get('gender')
                born_date = form.cleaned_data.get('born_date')
                enrollment_date = form.cleaned_data.get('enrollment_date')
                department_name = form.cleaned_data.get('department_name')
                major_name = form.cleaned_data.get('major_name')
                class_name = form.cleaned_data.get('class_name')

                models.Student.objects.filter(user__username=stu_id).update(name=name, gender=gender,
                                                                            born_date=born_date,
                                                                            enrollment_date=enrollment_date,
                                                                            department_name=department_name,
                                                                            major_name=major_name,
                                                                            class_name=class_name)
                return redirect('/stu/list/')
        return render(self.request, 'student_edit.html', {'form': form})


class ShowStuInfoService(IShowStuInfoService):
    def __init__(self, request):
        self.request = request

    def show_stu_info(self):
        value = self.request.GET.get('value', '')
        data_dict = {}
        if value:
            if value.isdigit():
                data_dict['user__username__contains'] = value
            else:
                data_dict['name__contains'] = value
        students = models.Student.objects.filter(**data_dict).order_by('user__username')

        page_obj = pagination.Pagination(self.request, students)

        context = {
            'value': value,

            'students': page_obj.page_queryset,
            'page_string': page_obj.html()
        }

        return render(self.request, 'student_show.html', context)


class ShowStuClassInfoService(IShowStuInClassInfoService):
    def __init__(self, request):
        self.request = request

    def show_stu_in_class_info(self, tp_id):
        value = self.request.GET.get('value', '')

        if value:
            if value.isdigit():
                students = models.Student.objects.filter(
                    Q(selectcourse__teaching_program_id=tp_id) & Q(user__username__contains=value)).order_by(
                    'user__username')

            else:
                students = models.Student.objects.filter(
                    Q(selectcourse__teaching_program_id=tp_id) & Q(name__contains=value)).order_by(
                    'user__username')
        else:
            students = models.Student.objects.filter(selectcourse__teaching_program_id=tp_id).order_by('user__username')

        page_obj = pagination.Pagination(self.request, students)

        context = {
            'value': value,

            'students': page_obj.page_queryset,
            'page_string': page_obj.html()
        }

        return render(self.request, 'student_in_class_list.html', context)


class ShowStuInPreviousClassService(IShowStuInPreviousClassService):
    def __init__(self, request):
        self.request = request

    def show_stu_in_previous_class_info(self, tp_id):
        value = self.request.GET.get('value', '')

        if value:
            if value.isdigit():
                students = models.Student.objects.filter(
                    Q(selectcourse__teaching_program_id=tp_id) & Q(user__username__contains=value) & Q(
                        selectcourse__grade__isnull=False)).values('user__username', 'name', 'gender',
                                                                   'department_name', 'major_name', 'class_name',
                                                                   'selectcourse__grade').order_by(
                    'user__username')

            else:
                students = models.Student.objects.filter(
                    Q(selectcourse__teaching_program_id=tp_id) & Q(name__contains=value) & Q(
                        selectcourse__grade__isnull=False)).values('user__username', 'name', 'gender',
                                                                   'department_name', 'major_name', 'class_name',
                                                                   'selectcourse__grade').order_by(
                    'user__username')
        else:
            students = models.Student.objects.filter(
                Q(selectcourse__teaching_program_id=tp_id) & Q(selectcourse__grade__isnull=False)) \
                .values('user__username',
                        'name',
                        'gender',
                        'department_name',
                        'major_name',
                        'class_name',
                        'selectcourse__grade').order_by(
                'user__username')

        page_obj = pagination.Pagination(self.request, students)

        context = {
            'value': value,

            'students': page_obj.page_queryset,
            'page_string': page_obj.html()
        }

        return render(self.request, 'student_in_previous_class.html', context)


class QueryGradeService(IQueryGradeService):
    def __init__(self, request):
        self.request = request

    def query_grade(self):
        value = self.request.GET.get('value', '')
        if value:
            selectcourses = models.SelectCourse.objects.filter(
                Q(teaching_program__course__course_name=value) & Q(grade__isnull=False)
                & Q(student__user__username=self.request.user.username)).values(
                'teaching_program__course__course_name',
                'teaching_program__teacher__name',
                'teaching_program__course__score',
                'teaching_program__course__the_period',
                'teaching_program__course__exp_period',
                'teaching_program__course__category',
                'grade'
            )
        else:
            selectcourses = models.SelectCourse.objects.filter(
                Q(grade__isnull=False) & Q(student__user__username=self.request.user.username)).values(
                'teaching_program__course__course_name',
                'teaching_program__teacher__name',
                'teaching_program__course__score',
                'teaching_program__course__the_period',
                'teaching_program__course__exp_period',
                'teaching_program__course__category',
                'grade'
            )
        page_obj = pagination.Pagination(self.request, selectcourses)
        context = {
            'value': value,
            'selectcourses': page_obj.page_queryset,
            'page_string': page_obj.html()
        }
        return render(self.request, 'query_grade.html', context)
