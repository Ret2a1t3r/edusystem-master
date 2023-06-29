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
from course import CourseForm

from school import models
from school.utils import pagination, bootstrap

from course_Interface import IAddCourseService, IShowCourseInfoService, IArrangingCourseService, IDeleteCourseService, \
    ISelectCourseService, IShowTeachTimeTableService, IShowPreviousTeachingCourseInfoService, IRecordScoreService, \
    IShowStuTimeTableService


class ShowCourseInfoService(IShowCourseInfoService):
    def __init__(self, request):
        self.request = request

    def show_course_info(self):
        value = self.request.GET.get('value', '')
        is_free = 0
        if not models.CourseArrangement.objects.all():
            is_free = 1
        if value:
            queryset = models.CourseArrangement.objects.filter(Q(teaching_program__teacher__name=value) |
                                                               Q(teaching_program__course__course_name__contains=value)) \
                .values('teaching_program__course__course_name',
                        'teaching_program__teacher__name',
                        'teaching_program__the_start_week',
                        'teaching_program__the_end_week',
                        'teaching_program__exp_start_week',
                        'teaching_program__exp_end_week',
                        'type',
                        'room__room_name', 'time__day', 'time__lesson') \
                .distinct().order_by('teaching_program__course__course_name')

        else:
            queryset = models.CourseArrangement.objects.filter().values('teaching_program__course__course_name',
                                                                        'teaching_program__teacher__name',
                                                                        'teaching_program__the_start_week',
                                                                        'teaching_program__the_end_week',
                                                                        'teaching_program__exp_start_week',
                                                                        'teaching_program__exp_end_week',
                                                                        'type',
                                                                        'room__room_name', 'time__day', 'time__lesson') \
                .distinct().order_by('teaching_program__course__course_name')

        page_obj = pagination.Pagination(self.request, queryset)

        context = {
            'value': value,

            'courses': page_obj.page_queryset,
            'page_string': page_obj.html(),
            'is_free': is_free
        }

        return render(self.request, 'course_list.html', context)


class AddCourseService(IAddCourseService):
    def __init__(self, request):
        self.request = request

    def course_add(self):
        if self.request.method == "GET":
            course_form = CourseForm()
            return render(self.request, 'course_add.html', {'courseForm': course_form})
        else:
            form = CourseForm(self.request.POST)
            if form.is_valid():
                course_name = form.cleaned_data.get('course_name')
                teacher = form.cleaned_data.get('teacher')
                start_week = int(form.cleaned_data.get('start_week'))
                end_week = int(form.cleaned_data.get('end_week'))
                day = form.cleaned_data.get('day')
                lesson = form.cleaned_data.get('lesson')
                building_name = form.cleaned_data.get('building_name')
                room_number = form.cleaned_data.get('room_number')
                max_volume = form.cleaned_data.get('max_volume')
                room_name = building_name + '-' + room_number

                weeks = ['第1周', '第2周', '第3周', '第4周', '第5周', '第6周',
                         '第7周', '第8周', '第9周', '第10周', '第11周', '第12周',
                         '第13周', '第14周', '第15周', '第16周', '第17周', '第18周']

                models.TeachingProgram.objects.create(
                    course=models.Course.objects.filter(course_name=course_name).first(),
                    teacher=models.Teacher.objects.filter(name=teacher).first(),
                    max_volume=max_volume,
                    the_start_week=weeks[start_week], the_end_week=weeks[end_week])
                teaching_program = models.TeachingProgram.objects.filter(course__course_name=course_name,
                                                                         teacher__name=teacher,
                                                                         start_week=weeks[start_week],
                                                                         end_week=weeks[end_week]).first()

                for i in range(start_week, end_week + 1):
                    models.CourseArrangement.objects.create(teaching_program=teaching_program,
                                                            room=models.Room.objects.filter(
                                                                room_name=room_name).first(),
                                                            time=models.Time.objects.filter(week=weeks[i], day=day,
                                                                                            lesson=lesson).first())
                return redirect('/course/list')
            else:
                return render(self.request, 'course_add.html', {'courseForm': form})


class DeleteCourseService(IDeleteCourseService):
    def __init__(self, request):
        self.request = request

    def course_delete(self):
        delete_data = str(self.request.GET.get('uid'))
        course_name, teacher_name, room_name, start_week, end_week, day, lesson = delete_data.split('|')
        print(course_name, teacher_name, room_name, start_week, end_week, day, lesson)

        weeks = ['第1周', '第2周', '第3周', '第4周', '第5周', '第6周',
                 '第7周', '第8周', '第9周', '第10周', '第11周', '第12周',
                 '第13周', '第14周', '第15周', '第16周', '第17周', '第18周']

        start = weeks.index(start_week)
        end = weeks.index(end_week)

        for i in range(start, end + 1):
            models.CourseArrangement.objects.filter(teaching_program__course__course_name=course_name,
                                                    teaching_program__teacher__name=teacher_name,
                                                    room__room_name=room_name,
                                                    time__week=weeks[i], time__day=day,
                                                    time__lesson=lesson).delete()
        return JsonResponse({
            'status': True,
        })


class ArrangingCourseService(IArrangingCourseService):
    def __init__(self, request):
        self.request = request

    def arranging_course(self):
        if self.request.method == 'GET':
            return render(self.request, 'arranging_course.html')
        names = ['软件必修.csv', '计算机必修.csv', '物联网必修.csv', '专业选修.csv', '专业班级信息.csv', '其他院排好的课.csv',
                 '同时间片课程.csv', '带实验.csv', '排好的课的文件.csv', '教室信息.csv', '老师信息.csv', '教师时间表.csv', '教师需求上课时间表.csv']

        files = []
        for i in range(13):
            t = self.request.FILES.get(str(i + 1))
            files.append(t)
        for i in range(13):
            f = open(names[i], mode='wb')
            for chunk in files[i].chunks():
                f.write(chunk)
            f.close()
        run.run()
        return redirect("/course/list")


class SelectCourseService(ISelectCourseService):
    def __init__(self, request):
        self.request = request

    def select_course(self):
        stu_id = self.request.user.username
        stu_class = models.Student.objects.filter(user__username=stu_id).first().class_name

        if self.request.method == 'GET':
            value = self.request.GET.get('value', '')

            selects = models.SelectCourse.objects.filter(student__user__username=stu_id)
            print(selects)
            times = models.Time.objects.filter(coursearrangement__teaching_program__selectcourse__in=selects)
            print(times)

            if value:
                queryset = models.CourseArrangement.objects.filter(Q(teacher__user_id=teach_id) &
                                                                   Q(course__course_name__contains=value) &
                                                                   Q(selectcourse__grade__isnull=False) &
                                                                   Q(type=1)) \
                    .values(
                    'id',
                    'course__course_name',
                    'teacher__name',
                    'start_week',
                    'end_week',
                    'classes') \
                    .distinct().order_by('course__course_name')

            # 'teaching_program__course__course_name',
            # 'teaching_program__course__score',
            # 'teaching_program__teacher__name',
            # 'room__room_name',
            # 'teaching_program__start_week',
            # 'teaching_program__end_week',
            # 'time__day',
            # 'time__lesson'

            else:
                arrangements = models.CourseArrangement.objects.filter(
                    Q(teaching_program__course__category=2) & ~Q(time__in=times) & Q(
                        teaching_program__classes__contains=stu_class)).values(
                    'teaching_program__course__course_name',
                    'teaching_program__course__score',
                    'teaching_program__teacher__name',
                    'room__room_name',
                    'teaching_program__course__the_period',
                    'teaching_program__course__exp_period',
                    'teaching_program__the_start_week',
                    'teaching_program__the_end_week',
                    'teaching_program__exp_start_week',
                    'teaching_program__exp_end_week',
                    'time__day',
                    'time__lesson',
                    'type') \
                    .distinct().order_by('teaching_program__course__course_name')

                count = {}
                data = {}
                pre_key = ''
                for arrangement in arrangements:
                    course_name = arrangement.get('teaching_program__course__course_name')
                    teacher_name = arrangement.get('teaching_program__teacher__name')
                    key = course_name + teacher_name

                    if key != pre_key:
                        the_period = int(arrangement.get('teaching_program__course__the_period'))
                        exp_period = int(arrangement.get('teaching_program__course__exp_period'))

                        the_start_week = arrangement['teaching_program__the_start_week']
                        the_end_week = arrangement['teaching_program__the_end_week']
                        exp_start_week = arrangement['teaching_program__exp_start_week']
                        exp_end_week = arrangement['teaching_program__exp_end_week']
                        if the_start_week:
                            the_start_week = int(the_start_week[1:the_start_week.find('周')])
                        else:
                            the_start_week = 0
                        if the_end_week:
                            the_end_week = int(the_end_week[1:the_end_week.find('周')])
                        else:
                            the_end_week = 0
                        if exp_start_week:
                            exp_start_week = int(exp_start_week[1:exp_start_week.find('周')])
                        else:
                            exp_start_week = 0
                        if exp_end_week:
                            exp_end_week = int(exp_end_week[1:exp_end_week.find('周')])
                        else:
                            exp_end_week = 0

                        data[key] = {'cnt': 1, 'course': arrangement['teaching_program__course__course_name'],
                                     'teacher_name': arrangement['teaching_program__teacher__name'],
                                     'score': arrangement['teaching_program__course__score'],
                                     'room_name': arrangement['room__room_name']}
                        if arrangement['type'] == 1:
                            data[key][
                                'time'] = arrangement['teaching_program__the_start_week'] + '-' + arrangement[
                                'teaching_program__the_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                              'time__lesson']
                        else:
                            data[key][
                                'time'] = arrangement['teaching_program__exp_start_week'] + '-' + arrangement[
                                'teaching_program__exp_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                              'time__lesson']

                        count[key] = 0
                        if the_start_week:
                            count[key] += the_period // (the_end_week - the_start_week) // 2
                        if exp_start_week:
                            count[key] += exp_period // (exp_end_week - exp_start_week) // 2
                        pre_key = key
                    else:
                        data[key]['cnt'] += 1
                        data[key]['room_name'] += '<br>' + arrangement['room__room_name']
                        if arrangement['type'] == 1:
                            data[key][
                                'time'] += '<br>' + arrangement['teaching_program__the_start_week'] + '-' + arrangement[
                                'teaching_program__the_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                               'time__lesson']
                        else:
                            data[key][
                                'time'] += '<br>' + arrangement['teaching_program__exp_start_week'] + '-' + arrangement[
                                'teaching_program__exp_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                               'time__lesson']

                delect_queue = []
                for key, val in data.items():
                    if count[key] != val['cnt']:
                        delect_queue.append(key)
                    else:
                        data[key]['room_name'] = mark_safe(data[key]['room_name'])
                        data[key]['time'] = mark_safe(data[key]['time'])
                for i in delect_queue:
                    data.pop(i)
                # for arrangement in arrangements:
                #     course_name, teacher_name, classes,
                # queryset = models.CourseArrangement.objects.filter(
                #     Q(teaching_program__course__category=2) & ~Q(time__in=times) & Q(
                #         teaching_program__classes__contains=stu_class)).values(
                #     'teaching_program__course__course_name',
                #     'teaching_program__course__score',
                #     'teaching_program__teacher__name',
                #     'room__room_name',
                #     'teaching_program__start_week',
                #     'teaching_program__end_week',
                #     'time__day',
                #     'time__lesson') \
                #     .distinct().order_by('teaching_program__course__course_name')

                # return JsonResponse({'query': queryset})
            # queryset = models.CourseArrangement.objects.filter(Q() & Q() & Q())

            page_obj = pagination.Pagination(self.request, arrangements)

            return render(self.request, 'select_course.html', {'courses': data})
        else:
            value = self.request.POST.get('uid')
            course_name, teacher_name = str(value).split('|')
            teaching_program = models.TeachingProgram.objects.filter(course__course_name=course_name,
                                                                     teacher__name=teacher_name,
                                                                     classes__contains=stu_class).first()
            stu = models.Student.objects.filter(user__username=stu_id).first()
            models.SelectCourse.objects.create(student=stu, teaching_program=teaching_program)
            return JsonResponse({
                'status': True,
            })


class ShowTeachTimeTableService(IShowTeachTimeTableService):
    def __init__(self, request):
        self.request = request

    def show_teach_time_table(self):
        value = self.request.GET.get('value', '')
        teach_id = self.request.user.id

        if value:
            arrangements = models.CourseArrangement.objects.filter(
                Q(teaching_program__teacher__user_id=teach_id) &
                Q(teaching_program__course__course_name__contains=value)).values(
                'teaching_program__course__course_name',
                'teaching_program__course__score',
                'teaching_program__teacher__name',
                'room__room_name',
                'teaching_program__course__the_period',
                'teaching_program__course__exp_period',
                'teaching_program__the_start_week',
                'teaching_program__the_end_week',
                'teaching_program__exp_start_week',
                'teaching_program__exp_end_week',
                'time__day',
                'time__lesson',
                'type') \
                .distinct().order_by('teaching_program__course__course_name')

        else:
            arrangements = models.CourseArrangement.objects.filter(
                Q(teaching_program__teacher__user_id=teach_id)).values(
                'teaching_program_id',
                'teaching_program__course__course_name',
                'teaching_program__course__score',
                'teaching_program__teacher__name',
                'room__room_name',
                'teaching_program__course__the_period',
                'teaching_program__course__exp_period',
                'teaching_program__the_start_week',
                'teaching_program__the_end_week',
                'teaching_program__exp_start_week',
                'teaching_program__exp_end_week',
                'time__day',
                'time__lesson',
                'type',
                'teaching_program__classes') \
                .distinct().order_by('teaching_program__course__course_name')

        data = {}
        pre_key = ""
        for arrangement in arrangements:
            course_name = arrangement.get('teaching_program__course__course_name')
            teacher_name = arrangement.get('teaching_program__teacher__name')
            classes = arrangement.get('teaching_program__classes')
            key = course_name + teacher_name + classes

            if key != pre_key:

                data[key] = {'cnt': 1, 'course': arrangement['teaching_program__course__course_name'],
                             'teacher_name': arrangement['teaching_program__teacher__name'],
                             'score': arrangement['teaching_program__course__score'],
                             'room_name': arrangement['room__room_name'],
                             'classes': arrangement['teaching_program__classes'],
                             'teaching_program_id': arrangement['teaching_program_id']}
                if arrangement['type'] == 1:
                    data[key][
                        'time'] = arrangement['teaching_program__the_start_week'] + '-' + arrangement[
                        'teaching_program__the_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                      'time__lesson']
                else:
                    data[key][
                        'time'] = arrangement['teaching_program__exp_start_week'] + '-' + arrangement[
                        'teaching_program__exp_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                      'time__lesson']
                pre_key = key
            else:
                data[key]['cnt'] += 1
                data[key]['room_name'] += '<br>' + arrangement['room__room_name']
                if arrangement['type'] == 1:
                    data[key][
                        'time'] += '<br>' + arrangement['teaching_program__the_start_week'] + '-' + arrangement[
                        'teaching_program__the_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                       'time__lesson']
                else:
                    data[key][
                        'time'] += '<br>' + arrangement['teaching_program__exp_start_week'] + '-' + arrangement[
                        'teaching_program__exp_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                       'time__lesson']
        for key, val in data.items():
            data[key]['room_name'] = mark_safe(data[key]['room_name'])
            data[key]['time'] = mark_safe(data[key]['time'])

        return render(self.request, 'teach_time_table.html', {'courses': data})


class ShowPreviousTeachingCourseInfoService(IShowPreviousTeachingCourseInfoService):
    def __init__(self, request):
        self.request = request

    def show_previous_teaching_course_info(self):
        value = self.request.GET.get('value', '')
        teach_id = self.request.user.id

        if value:
            queryset = models.TeachingProgram.objects.filter(Q(teacher__user_id=teach_id) &
                                                             Q(course__course_name__contains=value) &
                                                             Q(selectcourse__grade__isnull=False) &
                                                             Q(the_start_week__isnull=False)) \
                .values(
                'id',
                'course__course_name',
                'teacher__name',
                'the_start_week',
                'the_end_week',
                'classes') \
                .distinct().order_by('course__course_name')

        else:
            queryset = models.TeachingProgram.objects.filter(Q(teacher__user_id=teach_id) &
                                                             Q(selectcourse__grade__isnull=False) &
                                                             Q(the_start_week__isnull=False)
                                                             ).values(
                'id',
                'course__course_name',
                'teacher__name',
                'the_start_week',
                'the_end_week',
                'classes') \
                .distinct().order_by('course__course_name')

        page_obj = pagination.Pagination(self.request, queryset)

        context = {
            'value': value,

            'courses': page_obj.page_queryset,
            'page_string': page_obj.html()
        }

        return render(self.request, 'teacher_previous_course.html', context)


class RecordScoreService(IRecordScoreService):
    def __init__(self, request):
        self.request = request

    def score_record(self, tp_id):
        if self.request.method == "GET":
            students = models.Student.objects.filter(selectcourse__teaching_program_id=tp_id).order_by('user__username')

            return render(self.request, 'score_record.html', {'students': students})

        else:
            students = models.Student.objects.filter(selectcourse__teaching_program_id=tp_id)
            for student in students:
                grade = self.request.POST.get(student.user.username)
                models.SelectCourse.objects.filter(student=student, teaching_program_id=tp_id).update(grade=grade)
            models.CourseArrangement.objects.filter(teaching_program_id=tp_id).delete()
            return redirect('/course/list2')


class ShowStuTimeTableService(IShowStuTimeTableService):
    def __init__(self, request):
        self.request = request

    def show_stu_time_table(self):
        value = self.request.GET.get('value', '')
        stu_id = self.request.user.username

        if value:

            arrangements = models.CourseArrangement.objects.filter(
                Q(teaching_program__selectcourse__student__user__username=stu_id) &
                Q(teaching_program__course__course_name__contains=value)).values(
                'teaching_program__course__course_name',
                'teaching_program__course__score',
                'teaching_program__teacher__name',
                'room__room_name',
                'teaching_program__course__the_period',
                'teaching_program__course__exp_period',
                'teaching_program__the_start_week',
                'teaching_program__the_end_week',
                'teaching_program__exp_start_week',
                'teaching_program__exp_end_week',
                'time__day',
                'time__lesson',
                'type') \
                .distinct().order_by('teaching_program__course__course_name')

        else:
            arrangements = models.CourseArrangement.objects.filter(
                Q(teaching_program__selectcourse__student__user__username=stu_id)).values(
                'teaching_program__course__course_name',
                'teaching_program__course__score',
                'teaching_program__teacher__name',
                'room__room_name',
                'teaching_program__course__the_period',
                'teaching_program__course__exp_period',
                'teaching_program__the_start_week',
                'teaching_program__the_end_week',
                'teaching_program__exp_start_week',
                'teaching_program__exp_end_week',
                'time__day',
                'time__lesson',
                'type') \
                .distinct().order_by('teaching_program__course__course_name')

        data = {}
        pre_key = ""
        for arrangement in arrangements:
            course_name = arrangement.get('teaching_program__course__course_name')
            teacher_name = arrangement.get('teaching_program__teacher__name')
            key = course_name + teacher_name

            if key != pre_key:

                data[key] = {'cnt': 1, 'course': arrangement['teaching_program__course__course_name'],
                             'teacher_name': arrangement['teaching_program__teacher__name'],
                             'score': arrangement['teaching_program__course__score'],
                             'room_name': arrangement['room__room_name']}
                if arrangement['type'] == 1:
                    data[key][
                        'time'] = arrangement['teaching_program__the_start_week'] + '-' + arrangement[
                        'teaching_program__the_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                      'time__lesson']
                else:
                    data[key][
                        'time'] = arrangement['teaching_program__exp_start_week'] + '-' + arrangement[
                        'teaching_program__exp_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                      'time__lesson']
                pre_key = key
            else:
                data[key]['cnt'] += 1
                data[key]['room_name'] += '<br>' + arrangement['room__room_name']
                if arrangement['type'] == 1:
                    data[key][
                        'time'] += '<br>' + arrangement['teaching_program__the_start_week'] + '-' + arrangement[
                        'teaching_program__the_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                       'time__lesson']
                else:
                    data[key][
                        'time'] += '<br>' + arrangement['teaching_program__exp_start_week'] + '-' + arrangement[
                        'teaching_program__exp_end_week'] + ' ' + arrangement['time__day'] + ' ' + arrangement[
                                       'time__lesson']
        for key, val in data.items():
            data[key]['room_name'] = mark_safe(data[key]['room_name'])
            data[key]['time'] = mark_safe(data[key]['time'])

        return render(self.request, 'student_time_table.html', {'courses': data})