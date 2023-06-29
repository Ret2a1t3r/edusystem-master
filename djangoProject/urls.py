"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from school.views import create, student, account, teacher, room, course, chart, temp

urlpatterns = [
    # 后台管理员
    path('admin/', admin.site.urls),
    # 调试
    path('create/table/', create.create_table),

    # 查看学生信息
    path('stu/list/', student.stu_list),
    # 查看上课学生信息
    path('course/now/<int:tp_id>/list/', student.stu_in_class_list),
    # 查看历史课程信息
    path('course/previous/<int:tp_id>/list/', student.stu_in_previous_class_list),
    # 添加学生信息
    path('stu/add/', student.stu_add),
    # 删除学生信息
    path('stu/delete/', student.stu_delete),
    # 修改学生信息
    path('stu/<int:stu_id>/edit/', student.stu_edit),
    # 查看学生成绩
    path('stu/grade/',student.query_grade),

    # 查看教师信息
    path('teach/list/', teacher.teach_list),
    # 添加教师信息
    path('teach/add/', teacher.teach_add),
    # 删除教师信息
    path('teach/delete/', teacher.teach_delete),
    # 修改教师信息
    path('teach/<int:teach_id>/edit/', teacher.teach_edit),

    # 查看教室信息
    path('room/list/', room.room_list),
    # 添加教室信息
    path('room/add/', room.room_add),
    # 删除教室信息
    path('room/delete/', room.room_delete),
    # 修改教室信息
    path('room/<int:room_id>/edit/', room.room_edit),

    # 查看全部课程信息
    path('course/list/', course.course_list),
    # 查看教师当前学期课程信息
    path('teach/course/list/', course.show_teach_time_table),
    # 查看教师历史学期课程信息
    path('teach/course/previous/list/', course.previous_teaching_course_list),
    # 查看学生当前学期课程信息
    path('stu/course/list/', course.show_stu_time_table),
    # 添加课程信息
    path('course/add/', course.course_add),
    # 删除课程信息
    path('course/delete/', course.course_delete),

    # 课程分析
    path('manager/chart/list/', chart.manager_analysis_achievement),
    path('teach/chart/list/', chart.teach_analysis_achievement),
    path('chart/bar/', chart.char_bar),

    # 排课
    path('scheduling/course/', course.arranging_course),

    # 选课
    path('select/course/', course.select_course),

    # 登录
    path('',account.sign_in),
    path('login/', account.sign_in),
    path('logout/', account.sign_out),

    # 修改密码
    path('modify/pwd/', account.get_modify_pwd_page),
    path('modify/password/', account.modify_password),

    # 录入成绩
    path('score/<int:tp_id>/record/', course.score_record),

]
