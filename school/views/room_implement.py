from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from django.shortcuts import render, redirect

from school import models
from school.utils import pagination, bootstrap
from school.views.create import create_stu_id
from django.contrib.auth.decorators import login_required
from room_Interface import IEditRoomService, IDeleteRoomService, IAddRoomService, IShowRoomInfoService
from room import AddRoomForm, EditRoomForm


class ShowRoomInfoService(IShowRoomInfoService):
    def __init__(self, request):
        self.request = request

    def show_room_info(self):
        value = self.request.GET.get('value', '')
        data_dict = {}
        if value:
            data_dict['room_name__contains'] = value
        rooms = models.Room.objects.filter(**data_dict).order_by('room_name')

        page_obj = pagination.Pagination(self.request, rooms)

        context = {
            'value': value,

            'rooms': page_obj.page_queryset,
            'page_string': page_obj.html()
        }

        return render(self.request, 'room_list.html', context)


class AddRoomService(IAddRoomService):
    def __init__(self, request):
        self.request = request

    def room_add(self):
        if self.request.method == "GET":
            room_form = AddRoomForm()
            return render(self.request, 'room_add.html', {'roomForm': room_form})
        else:
            form = AddRoomForm(self.request.POST)
            if form.is_valid():

                building_name = form.cleaned_data.get('building_name')
                room_number = form.cleaned_data.get('room_number')
                room_name = building_name + '-' + room_number
                department = form.cleaned_data.get('department')
                volume = form.cleaned_data.get('volume')

                models.Room.objects.create(room_name=room_name, department=department, volume=volume)
                return redirect('/room/list')
            else:
                return render(self.request, 'room_add.html', {'roomForm': form})


class DeleteRoomService(IDeleteRoomService):
    def __init__(self, request):
        self.request = request

    def room_delete(self):
        room_id = self.request.GET.get('uid')
        models.Room.objects.filter(id=room_id).delete()
        return JsonResponse({
            'status': True,
        })


class EditRoomService(IEditRoomService):
    def __init__(self, request):
        self.request = request

    def room_edit(self, room_id):
        if self.request.method == 'GET':
            row_object = models.Room.objects.filter(id=room_id).first()
            position = row_object.room_name.find('-')
            building_name = row_object.room_name[: position]
            room_number = row_object.room_name[position + 1:]
            department = row_object.department
            volume = row_object.volume

            room_form = EditRoomForm(initial={'building_name': building_name, 'room_number': room_number,
                                              'department': department, 'volume': volume})
            return render(self.request, 'room_edit.html', {'roomForm': room_form})

        else:
            form = EditRoomForm(self.request.POST)
            if form.is_valid():
                building_name = form.cleaned_data.get('building_name')
                room_number = form.cleaned_data.get('room_number')
                department = form.cleaned_data.get('department')
                volume = form.cleaned_data.get('volume')

                room_name = building_name + '-' + room_number
                models.Room.objects.filter(id=room_id).update(room_name=room_name, department=department, volume=volume)
                return redirect('/room/list/')
        return render(self.request, 'room_edit.html', {'roomForm': form})

