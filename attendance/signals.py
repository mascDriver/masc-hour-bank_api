from datetime import timedelta, datetime

import pandas as pd
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from attendance.models import AttendanceDay, AttendanceMonth


@receiver(m2m_changed, sender=AttendanceDay.attendance_hour.through, dispatch_uid='att_hours_worked_day')
def att_hours_worked_day(sender, instance, **kwargs):
    if not instance.pk:
        return timedelta(seconds=0)
    if instance.attendance_hour.count() % 2 != 0:
        return timedelta(seconds=0)
    time_working = 0
    for cont, register_time in enumerate(instance.attendance_hour.all()):
        if cont % 2 != 0:
            continue
        if instance.employee_shift.work_shift.tolerance_time and register_time.hour.hour == instance.employee_shift.work_shift.entry1.hour and (
                pd.Timedelta(
                    register_time.hour.isoformat()).total_seconds() - instance.employee_shift.work_shift.tolerance_time.second <= pd.Timedelta(
            instance.employee_shift.work_shift.entry1.isoformat()).total_seconds() or pd.Timedelta(
            register_time.hour.isoformat()).total_seconds() + instance.employee_shift.work_shift.tolerance_time.second <= pd.Timedelta(
            instance.employee_shift.work_shift.entry1.isoformat()).total_seconds()):
            entry = datetime.combine(instance.day, instance.employee_shift.work_shift.entry1)
        elif instance.employee_shift.work_shift.tolerance_time and register_time.hour.hour == instance.employee_shift.work_shift.entry2.hour and (
                pd.Timedelta(
                    register_time.hour.isoformat()).total_seconds() - instance.employee_shift.work_shift.tolerance_time.second <= pd.Timedelta(
            instance.employee_shift.work_shift.entry2.isoformat()).total_seconds() or pd.Timedelta(
            register_time.hour.isoformat()).total_seconds() + instance.employee_shift.work_shift.tolerance_time.second <= pd.Timedelta(
            instance.employee_shift.work_shift.entry2.isoformat()).total_seconds()):
            entry = datetime.combine(instance.day, instance.employee_shift.work_shift.entry2)
        else:
            entry = datetime.combine(instance.day, register_time.hour)
        exit = datetime.combine(instance.day,
                                instance.get_next_or_prev(instance.attendance_hour.all(), register_time, 'next').hour)
        time_working += (exit - entry).seconds
    instance.worked_total = (datetime.min + timedelta(seconds=time_working)).time()
    instance.save()
    if AttendanceMonth.objects.filter(attendance_day=instance).exists():
        AttendanceMonth.objects.get(attendance_day=instance).save()



@receiver(post_save, sender=AttendanceMonth, dispatch_uid='att_hours_worked_month')
def att_hours_worked_month(sender, instance, **kwargs):
    time_working = 0
    for cont, attendance_day in enumerate(instance.attendance_day.all()):
        time_working += pd.Timedelta(attendance_day.worked_total.isoformat()).total_seconds()
    AttendanceMonth.objects.filter(pk=instance.pk).update(worked_total=time_working)
