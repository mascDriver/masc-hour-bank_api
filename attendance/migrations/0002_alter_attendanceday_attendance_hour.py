# Generated by Django 4.0.5 on 2022-07-07 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendanceday',
            name='attendance_hour',
            field=models.ManyToManyField(related_name='attendance_hour', to='attendance.attendancehour', verbose_name='Hour registered'),
        ),
    ]
