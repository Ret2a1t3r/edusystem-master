from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from django.shortcuts import render, redirect

from school import models
from school.utils import pagination, bootstrap
from school.views.create import create_stu_id
from django.contrib.auth.decorators import login_required

from room_implement import ShowRoomInfoService, AddRoomService, DeleteRoomService, EditRoomService


class AddRoomForm(bootstrap.BootStrapForm):
    building_name = forms.CharField(label='楼名')
    room_number = forms.CharField(label='教室号')
    department = forms.CharField(label="系")
    volume = forms.IntegerField(label="容量")

    def clean_building_name(self):
        building_name = self.cleaned_data['building_name']
        if not models.Room.objects.filter(room_name__contains=building_name):
            raise ValidationError('请输入正确的楼名。')
        return building_name

    def clean_room_number(self):
        building_name = self.cleaned_data['building_name']
        room_number = self.cleaned_data['room_number']
        room_name = building_name + '-' + room_number
        if models.Room.objects.filter(room_name=room_name):
            raise ValidationError('该教室记录已存在。')
        return room_number

    def clean_department(self):
        department = self.cleaned_data['department']
        print(department)
        if not models.Student.objects.filter(department_name=department):
            raise ValidationError('输入的系不存在。')
        return department

    def clean_volume(self):
        volume = self.cleaned_data['volume']
        if volume <= 0:
            raise ValidationError('请输入正确的教室容量。')
        return volume


class EditRoomForm(bootstrap.BootStrapForm):
    building_name = forms.CharField(label='楼名', widget=forms.TextInput(attrs={'readonly': True}))
    room_number = forms.CharField(label='教室号', widget=forms.TextInput(attrs={'readonly': True}))
    department = forms.CharField(label="系")
    volume = forms.IntegerField(label="容量", widget=forms.TextInput(attrs={'readonly': True}))

    def clean_department(self):
        department = self.cleaned_data['department']
        print(department)
        if not models.Student.objects.filter(department_name=department):
            raise ValidationError('输入的系不存在。')
        return department


class ShowRoomInfo:
    def __init__(self, cls):
        self.cls = cls

    def show_room_info(self):
        self.cls.show_room_info()


class AddRoom:
    def __init__(self, cls):
        self.cls = cls

    def room_add(self):
        self.cls.room_add()


class DeleteRoom:
    def __init__(self, cls):
        self.cls = cls

    def room_delete(self):
        self.cls.room_delete()


class EditRoom:
    def __init__(self, cls):
        self.cls = cls

    def room_edit(self, room_id):
        self.cls.room_edit(room_id)


@login_required
def room_list(request):
    show_room_info_service = ShowRoomInfoService(request)
    drive = ShowRoomInfo(show_room_info_service)
    return drive.show_room_info()


@login_required
def room_add(request):
    room_add_service = AddRoomService(request)
    drive = AddRoom(room_add_service)
    return drive.room_add()


@login_required
def room_delete(request):
    room_delete_service = DeleteRoomService(request)
    drive = DeleteRoom(room_delete_service)
    return drive.room_delete()


@login_required
def room_edit(request, room_id):
    room_edit_service = EditRoomService(request)
    drive = EditRoom(room_edit_service)
    return drive.room_edit(room_id)
