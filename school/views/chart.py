from django.shortcuts import render
from django.http import JsonResponse
from school import models
from chart_implement import ManagerCharInfoService, TeachCharInfoService, ShowChartInfoService

from datetime import datetime


class CharBar:
    def __init__(self, cls):
        self.cls = cls

    def show_chart_info(self):
        return self.cls.show_chart_info()


class AnalysisAchievementForManager:
    def __init__(self, cls):
        self.cls = cls

    def analysis_achievement(self):
        return self.cls.manager_analysis_achievement()


class AnalysisAchievementForTeacher:
    def __init__(self, cls):
        self.cls = cls

    def analysis_achievement(self):
        return self.cls.teach_analysis_achievement()


def manager_analysis_achievement(request):
    """教务人员课程分析"""
    manager_analysis_achievement = ManagerCharInfoService(request)
    drive = AnalysisAchievementForManager(manager_analysis_achievement)
    return drive.analysis_achievement()


def teach_analysis_achievement(request):
    """教师课程分析"""
    teach_analysis_achievement = TeachCharInfoService(request)
    drive = AnalysisAchievementForTeacher(teach_analysis_achievement)
    return drive.analysis_achievement()


def char_bar(request):
    """构造柱状图数据"""
    show_chart_info_service = ShowChartInfoService(request)
    drive = CharBar(show_chart_info_service)
    return drive.show_chart_info()
