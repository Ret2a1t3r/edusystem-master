from django.db.models import Q
from django.http import HttpResponse
from school.utils.analyse_teaching_program import analyse_teaching_program_csv, analyse_history_teaching_program_csv
from school.utils.analyse_course_arrangements import analyse_course_arrangements_csv
from school import models


def t1(request):
    models.Course.objects.all().delete()
    # models.User.objects.all().delete()
    # models.User.objects.filter(username='2004285').update(identify=1)

    # models.Room.objects.filter(Q(department='计算机科学与技术') | Q(department='物联网工程')).update(department='计算机')

    # arr = models.TeachingProgram.objects.all()
    # for i in arr:
    #     if models.CourseArrangement.objects.filter(teaching_program=i).count():
    #         i.delete()
    # analyse_history_teaching_program_csv(r"school/utils/专业选修.csv")
    # analyse_history_teaching_program_csv(r"school/utils/物联网必修.csv")
    # analyse_history_teaching_program_csv(r"school/utils/计算机必修.csv")
    # analyse_history_teaching_program_csv(r"school/utils/软件必修.csv")

    # analyse_teaching_program_csv(r"school/utils/专业选修.csv")
    # analyse_teaching_program_csv(r"school/utils/物联网必修.csv")
    # analyse_teaching_program_csv(r"school/utils/计算机必修.csv")
    # analyse_teaching_program_csv(r"school/utils/软件必修.csv")
    # analyse_course_arrangements_csv(r"school/utils/计算机.csv")
    # analyse_course_arrangements_csv(r"school/utils/软件.csv")
    return HttpResponse('Success')
