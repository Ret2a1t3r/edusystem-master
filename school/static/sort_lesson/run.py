import os
import time
from school.static.sort_lesson.analyse_teaching_program import  analyse_teaching_program_csv
from school.static.sort_lesson.analyse_course_arrangements import analyse_course_arrangements_csv


def run():
    t = os.getcwd()
    os.startfile(t + '\school\static\sort_lesson\排课程序.exe')
    analyse_teaching_program_csv(r"专业选修.csv")
    analyse_teaching_program_csv(r"物联网必修.csv")
    analyse_teaching_program_csv(r"计算机必修.csv")
    analyse_teaching_program_csv(r"软件必修.csv")
    analyse_course_arrangements_csv(r"计算机.csv")
    analyse_course_arrangements_csv(r"软件.csv")
    names = os.listdir()
    for i in names:
        path = i
        if path.find('.csv') != -1:
            os.remove(path)