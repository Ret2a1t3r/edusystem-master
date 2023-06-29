from chart_Interface import IShowAnalysisInfo, ITeachAnalysisAchievementService, IManagerAnalysisAchievementService
from django.shortcuts import render
from django.http import JsonResponse
from school import models
from datetime import datetime


class ShowChartInfoService(IShowAnalysisInfo):
    def __init__(self, request):
        self.request = request

    def show_analysis_info(self):
        """构造柱状图数据"""
        course_name = self.request.GET.get('course_name')

        queryset = models.TeachingProgram.objects.filter(course__course_name=course_name)

        if not queryset:
            return JsonResponse({
                'status': False
            })

        current_year = datetime.now().year

        can_year = 0
        for obj in queryset:
            select_set = obj.selectcourse_set.all()
            select = select_set.first()
            if select:
                year = int(select.student.enrollment_date.year)
                if select.grade:
                    can_year = max(can_year, year)

        st = current_year - can_year
        years = [(current_year - x) for x in range(st, st + 3)]

        legend = []

        for year in years:
            legend.append(str(year) + '级')

        x_list = ['0-35', '36-59', '60-69', '70-79', '80-89', '90-100']

        text = '《' + course_name + '》 成绩分析'

        data = [{}, {}, {}]

        for d in data:
            for x in x_list:
                d[x] = 0

        for obj in queryset:
            select_set = obj.selectcourse_set.all()
            for select in select_set:
                if select.grade:
                    year = int(select.student.enrollment_date.year)
                    grade = int(select.grade)

                    d = None
                    if year == years[0]:
                        d = data[0]

                    elif year == years[1]:
                        d = data[1]

                    elif year == years[2]:
                        d = data[2]

                    if d:
                        if grade <= 35:
                            d[x_list[0]] += 1
                        elif grade <= 59:
                            d[x_list[1]] += 1
                        elif grade <= 69:
                            d[x_list[2]] += 1
                        elif grade <= 79:
                            d[x_list[3]] += 1
                        elif grade <= 89:
                            d[x_list[4]] += 1
                        else:
                            d[x_list[5]] += 1

        series_list = [
            {
                'name': legend[0],
                'type': 'bar',
                'data': [x for x in data[0].values()]
            },
            {
                'name': legend[1],
                'type': 'bar',
                'data': [x for x in data[1].values()]
            },
            {
                'name': legend[2],
                'type': 'bar',
                'data': [x for x in data[2].values()]
            },
        ]

        dic = {
            'status': True,
            'data': {
                'text': text,
                'legend': legend,
                'series_list': series_list,
                'x_list': x_list,
            }
        }

        return JsonResponse(dic)


class TeachCharInfoService(ITeachAnalysisAchievementService):
    def __init__(self, request):
        self.request = request

    def teach_analysis_achievement(self):
        return render(self.request, 'teacher_analysis_achievement.html')


class ManagerCharInfoService(IManagerAnalysisAchievementService):
    def __init__(self, request):
        self.request = request

    def manager_analysis_achievement(self):
        return render(self.request, 'manager_analysis_achievement.html')
