from django.db import models

# 引用内置的user模型
from django.contrib.auth.models import AbstractUser


class Student(models.Model):
    """学生信息表"""

    gender_choice = (
        (1, "男"),
        (2, "女")
    )

    user = models.ForeignKey(to='User', verbose_name="学号", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="姓名", max_length=10)
    gender = models.CharField(verbose_name="性别", max_length=1, choices=gender_choice)
    born_date = models.DateField(verbose_name="出生日期")
    enrollment_date = models.DateField(verbose_name="入学日期")
    majorId= models.IntegerField(verbose_name="专业id", max_length=8)
    classId = models.IntegerField(verbose_name="班级id", max_length=8)

    def __str__(self):
        return self.name + " " + self.major_name + " " + self.class_name


class Teacher(models.Model):
    """教师信息表"""

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

    user = models.ForeignKey(to='User', verbose_name="工号", max_length=7, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="姓名", max_length=10)
    born_date = models.DateField(verbose_name="出生日期")
    entry_date = models.DateField(verbose_name="入职日期")
    title = models.CharField(verbose_name="职称", max_length=8, choices=title_choice, default=2)
    collegeId = models.ForeignKey(verbose_name="学院id", max_length=8)
    gender = models.CharField(verbose_name="性别", max_length=1, choices=gender_choice)

    def __str__(self):
        return self.name


class Course(models.Model):
    """课程信息表"""

    category_choice = (
        (1, "必修"),
        (2, "选修")
    )

    user = models.ForeignKey(to='Course', verbose_name="课程号", max_length=8, on_delete=models.CASCADE)
    course_name = models.CharField(verbose_name="课程名", max_length=10)
    score = models.SmallIntegerField(verbose_name="学分", max_length=2, decimal_places=1)
    the_period = models.SmallIntegerField(verbose_name="理论课学时", max_length=2, default=0)
    exp_period = models.SmallIntegerField(verbose_name="实验课学时", max_length=2, default=0)
    category = models.CharField(verbose_name="课程性质", max_length=1, choices=category_choice)

    def __str__(self):
        return self.course_name + "(" + self.get_category_display() + ")"


class ClassRoom(models.Model):
    """教室表"""
    class_number = models.CharField(verbose_name="教室号", max_length=8)
    spot = models.CharField(verbose_name="地点", max_length=10)
    volume = models.IntegerField(verbose_name="容纳人数", max_length=8)
    academyId = models.ForeignKey(to='academy', on_delete=models.CASCADE, verbose_name='学院Id')


class Academy(models.Model):
    """学院表"""
    major_name = models.CharField(verbose_name="学院名", max_length=20)


class Major(models.Model):
    """专业表"""
    major_name = models.CharField(verbose_name="专业名", max_length=20)
    academyId = models.ForeignKey(verbose_name="学院id", max_length=8)


class SchoolClass(models.Model):
    """班级表"""
    class_name = models.CharField(verbose_name="班级名", max_length=20)
    grade = models.CharField(verbose_name="年级", max_length=4)

    def __str__(self):
        return self.student.name + '：' + self.teaching_program.course.course_name


class Time(models.Model):
    """时间表"""
    week = models.CharField(verbose_name="周次", max_length=4)
    day = models.CharField(verbose_name="星期", max_length=4)
    lesson = models.CharField(verbose_name="节次", max_length=4)

    def __str__(self):
        return self.week + ' ' + self.day + ' ' + self.lesson


class TeachingProgram(models.Model):
    """教学计划表"""

    course = models.ForeignKey(to='Course', verbose_name='课程id', on_delete=models.CASCADE)
    teacherId = models.ForeignKey(to='Teacher', verbose_name='教师id', max_length=8, on_delete=models.CASCADE)
    classesId = models.ForeignKey(verbose_name='班级id', max_length=8, on_delete=models.CASCA)
    openTime = models.CharField(verbose_name='开设学期', max_length=1)
    the_start_week = models.CharField(verbose_name='理论课开始周次', max_length=4, null=True, blank=True)
    the_end_week = models.CharField(verbose_name='理论课结束周次', max_length=4, null=True, blank=True)
    exp_start_week = models.CharField(verbose_name='实验课开始周次', max_length=4, null=True, blank=True)
    exp_end_week = models.CharField(verbose_name='实验课结束周次', max_length=4, null=True, blank=True)

    def __str__(self):
        return self.course.course_name + ' ' + self.teacher.name + ' ' + self.classes


class RoomTime(models.Model):
    """教室时间表"""
    roomId = models.ForeignKey(verbose_name="教室id", max_length=8, unique=True)
    timeId = models.ForeignKey(verbose_name="时间id", max_length=8)

    def __str__(self):
        return self.room_name


class SelectCourse(models.Model):
    """选课表"""

    studentId = models.ForeignKey(to='Student', max_length=8, on_delete=models.CASCADE, verbose_name='学生id')
    teaching_programId = models.ForeignKey(to='TeachingProgram', max_length=8, on_delete=models.CASCADE, verbose_name='教学计划id', null=True,
                                         blank=True)
    gradeId = models.IntegerField(verbose_name='成绩id', max_length=8, null=True, blank=True)

    def __str__(self):
        return self.student.name + '：' + self.teaching_program.course.course_name


class CourseArrangement(models.Model):
    """课程安排表"""
    type_choic = (
        (1, '理论课'),
        (2, '实验课')
    )

    teaching_programID = models.ForeignKey(to='TeachingProgram', max_length=8, verbose_name='教学计划id', on_delete=models.CASCADE)
    roomTimeId = models.ForeignKey(to='Room', verbose_name='教室时间id', max_length=8, on_delete=models.CASCADE)
    tmp_volume = models.IntegerField(verbose_name='当前人数', max_length=8, default=0)

    def __str__(self):
        return self.teaching_program.course.course_name + " " + self.room.room_name + self.time.__str__()


# class Message(models.Model):
#     """消息表"""
#
#     message_id = models.CharField(max_length=20, verbose_name='消息号', primary_key=True, unique=True, db_index=True)
#     student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING, verbose_name='学号')
#     message_content = models.CharField(max_length=1000, verbose_name='消息内容')
#     message_send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送日期')
#     message_status = models.CharField(max_length=20, verbose_name='消息状态')
#     message_title = models.CharField(max_length=255, verbose_name='消息标题')