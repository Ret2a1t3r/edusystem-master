import os

from school.static.sort_lesson import run

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from school import models
from school.utils import pagination, bootstrap

from course_implement import ShowCourseInfoService, ShowPreviousTeachingCourseInfoService, ShowTeachTimeTableService, \
    ShowStuTimeTableService, SelectCourseService, AddCourseService, DeleteCourseService, ArrangingCourseService, \
    RecordScoreService


class CourseForm(bootstrap.BootStrapForm):
    week_choice = (
        (0, '第1周'),
        (1, '第2周'),
        (2, '第3周'),
        (3, '第4周'),
        (4, '第5周'),
        (5, '第6周'),
        (6, '第7周'),
        (7, '第8周'),
        (8, '第9周'),
        (9, '第10周'),
        (10, '第11周'),
        (11, '第12周'),
        (12, '第13周'),
        (13, '第14周'),
        (14, '第15周'),
        (15, '第16周'),
        (16, '第17周'),
        (17, '第18周'),
    )

    day_choice = (
        ('星期一', '星期一'),
        ('星期二', '星期二'),
        ('星期三', '星期三'),
        ('星期四', '星期四'),
        ('星期五', '星期五'),
        ('星期六', '星期六'),
        ('星期日', '星期日'),
    )

    lesson_choice = (
        ('1,2节', '1,2节'),
        ('3,4节', '3,4节'),
        ('5,6节', '5,6节'),
        ('7,8节', '7,8节'),
        ('9,10节', '9,10节'),
    )

    course_name = forms.CharField(label='课程名')
    teacher = forms.CharField(label='上课教师')
    day = forms.ChoiceField(label='上课星期', choices=day_choice, widget=forms.Select)
    lesson = forms.ChoiceField(label='上课节次', choices=lesson_choice, widget=forms.Select)
    start_week = forms.ChoiceField(label='开始周次', choices=week_choice, widget=forms.Select)
    end_week = forms.ChoiceField(label='结束周次', choices=week_choice, widget=forms.Select)

    building_name = forms.CharField(label='上课楼名')
    room_number = forms.CharField(label='上课教室号')
    max_volume = forms.IntegerField(label='上课人数')

    def clean_course_name(self):
        course_name = self.cleaned_data['course_name']
        if not models.Course.objects.filter(course_name=course_name):
            raise ValidationError('该课程不存在。')
        return course_name

    def clean_teacher(self):
        teacher = self.cleaned_data['teacher']
        if not models.Teacher.objects.filter(name=teacher):
            raise ValidationError('该教师不存在。')
        return teacher

    def clean_end_week(self):
        teacher = self.cleaned_data['teacher']
        start_week = self.cleaned_data['start_week']
        end_week = self.cleaned_data['end_week']
        day = self.cleaned_data['day']
        lesson = self.cleaned_data['lesson']

        weeks = ['第1周', '第2周', '第3周', '第4周', '第5周', '第6周',
                 '第7周', '第8周', '第9周', '第10周', '第11周', '第12周',
                 '第13周', '第14周', '第15周', '第16周', '第17周', '第18周']

        for i in range(int(start_week), int(end_week) + 1):
            if models.CourseArrangement.objects.filter(time__week=weeks[i], time__day=day, time__lesson=lesson,
                                                       teaching_program__teacher__name=teacher):
                raise ValidationError('此教师该时间段有课。')
        return end_week

    def clean_building_name(self):
        building_name = self.cleaned_data['building_name']
        if not models.Room.objects.filter(room_name__contains=building_name):
            raise ValidationError('请输入正确的楼名。')
        return building_name

    def clean_room_number(self):
        start_week = self.cleaned_data['start_week']
        if 'end_week' not in self.cleaned_data:
            return
        end_week = self.cleaned_data['end_week']
        day = self.cleaned_data['day']
        lesson = self.cleaned_data['lesson']
        building_name = self.cleaned_data['building_name']
        room_number = self.cleaned_data['room_number']
        room_name = building_name + '-' + room_number
        weeks = ['第1周', '第2周', '第3周', '第4周', '第5周', '第6周',
                 '第7周', '第8周', '第9周', '第10周', '第11周', '第12周',
                 '第13周', '第14周', '第15周', '第16周', '第17周', '第18周']

        if not models.Room.objects.filter(room_name=room_name):
            raise ValidationError('该教室不存在。')

        for i in range(int(start_week), int(end_week) + 1):
            if models.CourseArrangement.objects.filter(time__week=weeks[i], time__day=day, time__lesson=lesson,
                                                       room__room_name=room_name):
                raise ValidationError('此教室该时间段有课。')

        return room_number

    def clean_max_volume(self):
        max_volume = self.cleaned_data['max_volume']
        if max_volume <= 0:
            raise ValidationError('请输入正确的上课人数。')
        return max_volume


class SelectCourse:
    def __init__(self, cls):
        self.cls = cls

    def select_course(self):
        return self.cls.select_course()


class RecordScore:
    def __init__(self, cls):
        self.cls = cls

    def score_record(self, tp_id):
        return self.cls.score_record(tp_id)


class ArrangingCourse:
    def __init__(self, cls):
        self.cls = cls

    def arranging_course(self):
        return self.cls.arranging_course()


class ShowCourseInfo:
    def __init__(self, cls):
        self.cls = cls

    def show_course_info(self):
        return self.cls.show_course_info()


class AddCourse:
    def __init__(self, cls):
        self.cls = cls

    def course_add(self):
        return self.cls.course_add()


class ShowPreviousTeachingCourseInfo:
    def __init__(self, cls):
        self.cls = cls

    def show_previous_teaching_course_info(self):
        return self.cls.show_previous_teaching_course_info()


class ShowTeachTimeTable:
    def __init__(self, cls):
        self.cls = cls

    def show_teach_time_table(self):
        return self.cls.show_teach_time_table()


class ShowStuTimeTable:
    def __init__(self, cls):
        self.cls = cls

    def show_stu_time_table(self):
        return self.cls.show_stu_time_table()


class DeleteCourse:
    def __init__(self, cls):
        self.cls = cls

    def course_delete(self):
        return self.cls.coursE_delete()


@login_required
def course_list(request):
    show_course_service = ShowCourseInfoService(request)
    drive = ShowCourseInfo(show_course_service)
    return drive.show_course_info()


@login_required
def course_add(request):
    add_course_service = AddCourseService(request)
    drive = AddCourse(add_course_service)
    return drive.course_add()


@login_required
def course_delete(request):
    delete_course_service = AddCourseService(request)
    drive = DeleteCourse(delete_course_service)
    return drive.course_delete()


def arranging_course(request):
    arranging_course_service = ArrangingCourseService(request)
    drive = ArrangingCourse(arranging_course_service)
    return drive.arranging_course()


def show_teach_time_table(request):
    show_teach_time_table_service = ShowTeachTimeTableService(request)
    drive = ShowTeachTimeTable(show_teach_time_table_service)
    return drive.show_teach_time_table()


def show_stu_time_table(request):
    show_stu_time_table_service = ShowStuTimeTableService(request)
    drive = ShowStuTimeTable(show_stu_time_table_service)
    return drive.show_stu_time_table()


def previous_teaching_course_list(request):
    previous_teaching_course_service = ShowPreviousTeachingCourseInfoService(request)
    drive = ShowPreviousTeachingCourseInfo(previous_teaching_course_service)
    return drive.show_previous_teaching_course_info()


def score_record(request, tp_id):
    score_record_service = RecordScoreService(request)
    drive = RecordScore(score_record_service)
    return drive.score_record(tp_id)


@method_decorator(csrf_exempt)
def select_course(request):
    select_course_service = SelectCourseService(request)
    drive = SelectCourse(select_course_service)
    return drive.select_course()
