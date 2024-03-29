# Generated by Django 3.2.5 on 2022-04-04 14:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('identify', models.SmallIntegerField(choices=[(1, '教务人员'), (2, '老师'), (3, '学生')], default=3, verbose_name='身份')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=10, verbose_name='课程名')),
                ('score', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='学分')),
                ('the_period', models.SmallIntegerField(default=0, verbose_name='理论课学时')),
                ('exp_period', models.SmallIntegerField(default=0, verbose_name='实验课学时')),
                ('category', models.SmallIntegerField(choices=[(1, '必修'), (2, '选修')], verbose_name='课程性质')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=10, unique=True, verbose_name='教室')),
                ('department', models.CharField(max_length=20, verbose_name='系')),
                ('volume', models.SmallIntegerField(verbose_name='容量')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='姓名')),
                ('born_date', models.DateField(verbose_name='出生日期')),
                ('entry_date', models.DateField(verbose_name='入职日期')),
                ('title', models.SmallIntegerField(choices=[(1, '助教'), (2, '讲师'), (3, '副教授'), (4, '教授')], default=2, verbose_name='职称')),
                ('department_name', models.CharField(max_length=20, verbose_name='系')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='工号')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.CharField(max_length=5, verbose_name='周次')),
                ('day', models.CharField(max_length=5, verbose_name='星期')),
                ('lesson', models.CharField(max_length=5, verbose_name='节次')),
            ],
        ),
        migrations.CreateModel(
            name='TeachingProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.CharField(max_length=20, verbose_name='上课班级')),
                ('max_volume', models.SmallIntegerField(verbose_name='最大容量')),
                ('the_start_week', models.CharField(blank=True, max_length=5, null=True, verbose_name='理论课开始周次')),
                ('the_end_week', models.CharField(blank=True, max_length=5, null=True, verbose_name='理论课结束周次')),
                ('exp_start_week', models.CharField(blank=True, max_length=5, null=True, verbose_name='实验课开始周次')),
                ('exp_end_week', models.CharField(blank=True, max_length=5, null=True, verbose_name='实验课结束周次')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.course', verbose_name='课程')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teacher', verbose_name='上课教师')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='姓名')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('born_date', models.DateField(verbose_name='出生日期')),
                ('enrollment_date', models.DateField(verbose_name='入学日期')),
                ('department_name', models.CharField(max_length=20, verbose_name='系')),
                ('major_name', models.CharField(max_length=20, verbose_name='专业')),
                ('class_name', models.CharField(max_length=20, verbose_name='班级')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='学号')),
            ],
        ),
        migrations.CreateModel(
            name='SelectCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.SmallIntegerField(blank=True, null=True, verbose_name='成绩')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student', verbose_name='学生')),
                ('teaching_program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.teachingprogram', verbose_name='已选课程')),
            ],
        ),
        migrations.CreateModel(
            name='CourseArrangement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmp_volume', models.IntegerField(default=0, verbose_name='当前容量')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.room', verbose_name='上课地点')),
                ('teaching_program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teachingprogram', verbose_name='教学计划')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.time', verbose_name='上课时间')),
            ],
        ),
    ]
