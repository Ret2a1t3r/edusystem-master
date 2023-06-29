import csv
from school import models
import random
from django.db.models import Q


def analyse_history_teaching_program_csv(filename):
    category = 0
    if filename.find("必修") != -1:
        category = 1
    if filename.find("选修") != -1:
        category = 2
    if not category:
        return False
    with open(filename, 'r', encoding='ANSI') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "课程名称":
                continue
            print(row)
            for i in range(len(row)):
                row[i] = row[i].strip()
            if models.Course.objects.filter(course_name=row[0]).count() == 0:
                the_num, exp_num = 0, 0
                if row[4] != '0':
                    st = int(row[4].split('~')[0])
                    ed = int(row[4].split('~')[1])
                    the_num = (ed - st) * int(row[5])
                if row[6] != '0':
                    st = int(row[6].split('~')[0])
                    ed = int(row[6].split('~')[1])
                    exp_num = (ed - st) * int(row[7])
                score = 0
                if random.randint(0, 1):
                    score = 0.5
                score += random.randint(1, 5)
                if score == 5.5:
                    score = 5
                models.Course.objects.create(course_name=row[0], score=score, the_period=the_num, exp_period=exp_num,
                                             category=category)
            course = models.Course.objects.get(course_name=row[0])
            classes_temp = row[2].split('/')
            classes_name = ""
            classes_temp.sort()
            for i in classes_temp:
                if classes_name == "":
                    classes_name += i
                else:
                    classes_name += ',' + i
            teacher = models.Teacher.objects.get(name=row[1])
            max_volume = int(row[3])
            the_start_week = None
            exp_start_week = None
            the_end_week = None
            exp_end_week = None
            if row[4] != '0':
                the_start_week = "第" + row[4].split('~')[0] + '周'
                the_end_week = "第" + row[4].split('~')[1] + '周'
            if row[6] != '0':
                exp_start_week = "第" + row[6].split('~')[0] + '周'
                exp_end_week = "第" + row[6].split('~')[1] + '周'

            if models.TeachingProgram.objects.filter(course=course, teacher=teacher, classes=classes_name,
                                                     max_volume=max_volume, the_start_week=the_start_week,
                                                     the_end_week=the_end_week,
                                                     exp_start_week=exp_start_week, exp_end_week=exp_end_week):
                return False

            models.TeachingProgram.objects.create(course=course, teacher=teacher, classes=classes_name,
                                                  max_volume=max_volume, the_start_week=the_start_week,
                                                  the_end_week=the_end_week,
                                                  exp_start_week=exp_start_week, exp_end_week=exp_end_week)
            if category == 1:
                students = models.Student.objects.filter(class_name__in=classes_temp)

                t = models.TeachingProgram.objects.get(course=course, teacher=teacher, classes=classes_name,
                                                       max_volume=max_volume, the_start_week=the_start_week,
                                                       the_end_week=the_end_week,
                                                       exp_start_week=exp_start_week, exp_end_week=exp_end_week)
                for stu in students:
                    percent = random.randint(1, 1000)
                    if percent <= 20:
                        grade = random.randint(0, 35)
                    elif percent <= 120:
                        grade = random.randint(36, 59)
                    elif percent <= 520:
                        grade = random.randint(60, 69)
                    elif percent <= 800:
                        grade = random.randint(70, 79)
                    elif percent <= 950:
                        grade = random.randint(80, 89)
                    else:
                        grade = random.randint(90, 100)
                    models.SelectCourse.objects.create(student=stu, teaching_program=t, grade=grade)
            else:
                now_people_num = 0
                students = models.Student.objects.filter(class_name__in=classes_temp)
                t = models.TeachingProgram.objects.get(course=course, teacher=teacher, classes=classes_name,
                                                       max_volume=max_volume, the_start_week=the_start_week,
                                                       the_end_week=the_end_week,
                                                       exp_start_week=exp_start_week, exp_end_week=exp_end_week)
                choic_len = random.randint(1, 6)
                now_choic = random.randint(1, choic_len)
                cnt = 0
                for stu in students:
                    if now_people_num >= max_volume:
                        break
                    cnt = cnt + 1
                    if cnt == now_choic:
                        now_people_num = now_people_num + 1
                        percent = random.randint(1, 1000)
                        if percent <= 20:
                            grade = random.randint(0, 35)
                        elif percent <= 120:
                            grade = random.randint(36, 59)
                        elif percent <= 520:
                            grade = random.randint(60, 69)
                        elif percent <= 800:
                            grade = random.randint(70, 79)
                        elif percent <= 950:
                            grade = random.randint(80, 89)
                        else:
                            grade = random.randint(90, 100)
                        models.SelectCourse.objects.create(student=stu, teaching_program=t, grade=grade)
                        now_choic = random.randint(1, choic_len)
                    if cnt == choic_len:
                        cnt = 0
    return True


def analyse_teaching_program_csv(filename):
    category = 0
    if filename.find("必修") != -1:
        category = 1
    if filename.find("选修") != -1:
        category = 2
    if not category:
        return False
    with open(filename, 'r', encoding='ANSI') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "课程名称":
                continue
            print(row)
            for i in range(len(row)):
                row[i] = row[i].strip()
            if models.Course.objects.filter(course_name=row[0]).count() == 0:
                the_num, exp_num = 0, 0
                if row[4] != '0':
                    st = int(row[4].split('~')[0])
                    ed = int(row[4].split('~')[1])
                    the_num = (ed - st) * int(row[5])
                if row[6] != '0':
                    st = int(row[6].split('~')[0])
                    ed = int(row[6].split('~')[1])
                    exp_num = (ed - st) * int(row[7])
                score = 0
                if random.randint(0, 1):
                    score = 0.5
                score += random.randint(1, 5)
                if score == 5.5:
                    score = 5
                models.Course.objects.create(course_name=row[0], score=score, the_period=the_num, exp_period=exp_num,
                                             category=category)
            course = models.Course.objects.get(course_name=row[0])
            classes_temp = row[2].split('/')
            classes_name = ""
            classes_temp.sort()
            for i in classes_temp:
                if classes_name == "":
                    classes_name += i
                else:
                    classes_name += ',' + i
            teacher = models.Teacher.objects.get(name=row[1])
            max_volume = int(row[3])
            the_start_week = None
            exp_start_week = None
            the_end_week = None
            exp_end_week = None
            if row[4] != '0':
                the_start_week = "第" + row[4].split('~')[0] + '周'
                the_end_week = "第" + row[4].split('~')[1] + '周'
            if row[6] != '0':
                exp_start_week = "第" + row[6].split('~')[0] + '周'
                exp_end_week = "第" + row[6].split('~')[1] + '周'

            if models.TeachingProgram.objects.filter(course=course, teacher=teacher, classes=classes_name,
                                                     max_volume=max_volume,the_start_week=the_start_week, the_end_week=the_end_week,
                                                     exp_start_week=exp_start_week,exp_end_week=exp_end_week):
                return False

            models.TeachingProgram.objects.create(course=course, teacher=teacher, classes=classes_name,
                                                     max_volume=max_volume,the_start_week=the_start_week, the_end_week=the_end_week,
                                                     exp_start_week=exp_start_week,exp_end_week=exp_end_week)
            if category == 1:
                students = models.Student.objects.filter(class_name__in=classes_temp)
                t = models.TeachingProgram.objects.get(course=course, teacher=teacher, classes=classes_name,
                                                     max_volume=max_volume,the_start_week=the_start_week, the_end_week=the_end_week,
                                                     exp_start_week=exp_start_week,exp_end_week=exp_end_week)
                for stu in students:
                    percent = random.randint(1, 1000)
                    if percent <= 20:
                        grade = random.randint(0, 35)
                    elif percent <= 120:
                        grade = random.randint(36, 59)
                    elif percent <= 520:
                        grade = random.randint(60, 69)
                    elif percent <= 800:
                        grade = random.randint(70, 79)
                    elif percent <= 950:
                        grade = random.randint(80, 89)
                    else:
                        grade = random.randint(90, 100)
                    models.SelectCourse.objects.create(student=stu, teaching_program=t, grade=grade)



    return True
