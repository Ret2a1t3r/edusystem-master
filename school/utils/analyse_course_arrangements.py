import csv
from school import models
import random

def analyse_course_arrangements_csv(filename):
    dict={'1':'一','2':'二','3':'三','4':'四','5':'五','6':'六','7':'日'}
    with open(filename, 'r', encoding='ANSI') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "学院":
                continue
            print(row)
            for i in range(len(row)):
                row[i] = row[i].strip()
            course_name = row[3]
            teacher_name = row[4]
            classes_temp = row[5].split('/')
            classes_name = ""
            classes_temp.sort()
            for i in classes_temp:
                if classes_name == "":
                    classes_name += i
                else:
                    classes_name += ',' + i

            week_st = int(row[8].split('-')[0])
            week_ed = int(row[8].split('-')[1].split('周')[0])

            if row[12] == '0':
                teachingprogram = models.TeachingProgram.objects.get(course__course_name=course_name,
                                                                     teacher__name=teacher_name,
                                                                     classes=classes_name,
                                                                     the_start_week="第%d" % week_st + "周",
                                                                     the_end_week="第%d" % week_ed + "周")
                room = models.Room.objects.get(room_name=row[7])
                for i in range(week_st,week_ed+1):
                    time = models.Time.objects.get(week="第%d"%i+"周",day="星期"+dict[row[9]],lesson=row[10]+","+row[11]+"节")
                    if models.CourseArrangement.objects.filter(teaching_program=teachingprogram,room=room,time=time).count():
                        return False
                    models.CourseArrangement.objects.create(teaching_program=teachingprogram, room=room, time=time)
            else:
                teachingprogram = models.TeachingProgram.objects.get(course__course_name=course_name,
                                                                     teacher__name=teacher_name,
                                                                     classes=classes_name,
                                                                     exp_start_week="第%d" % week_st + "周",
                                                                     exp_end_week="第%d" % week_ed + "周")
                while(True):
                    flag = True
                    room_num = random.randint(1, 6) * 100 + random.randint(0, 2) * 10 + random.randint(0, 9)
                    room = models.Room.objects.get(room_name=row[7]+"%d"%room_num)
                    for i in range(week_st, week_ed + 1):
                        time = models.Time.objects.get(week="第%d" % i + "周", day="星期" + dict[row[9]],
                                                       lesson=row[10] + "," + row[11] + "节")
                        if models.CourseArrangement.objects.filter(time=time,room=room):
                            flag=False
                            break
                    if flag:
                        for i in range(week_st, week_ed + 1):
                            time = models.Time.objects.get(week="第%d" % i + "周", day="星期" + dict[row[9]],
                                                           lesson=row[10] + "," + row[11] + "节")
                            if models.CourseArrangement.objects.filter(teaching_program=teachingprogram, room=room,
                                                                       time=time).count():
                                return False
                            models.CourseArrangement.objects.create(teaching_program=teachingprogram, room=room,
                                                                    time=time)
                        break