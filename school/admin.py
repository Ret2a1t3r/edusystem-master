from django.contrib import admin

# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     pass
#
#
# admin.site.register(models.User, UserAdmin)
from school import models
from django.contrib.auth.admin import UserAdmin

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Room)
admin.site.register(models.Course)
admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.CourseArrangement)
admin.site.register(models.SelectCourse)
admin.site.register(models.Time)
admin.site.register(models.TeachingProgram)
