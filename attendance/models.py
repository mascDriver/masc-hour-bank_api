from calendar import month_name
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class WorkShift(models.Model):
    name = models.CharField(verbose_name=_('Name of work shift'), max_length=100, null=True, blank=True)
    tolerance_time = models.TimeField(verbose_name=_("Tolerance time"), null=True, blank=True)
    entry1 = models.TimeField(verbose_name=_('Fisrt entry'))
    exit1 = models.TimeField(verbose_name=_('First exit'))
    entry2 = models.TimeField(verbose_name=_('Second entry'))
    exit2 = models.TimeField(verbose_name=_('Second exit'))
    entry3 = models.TimeField(verbose_name=_('Optional entry'), null=True, blank=True)
    exit3 = models.TimeField(verbose_name=_('Optional exit'), null=True, blank=True)

    def __str__(self):
        if self.name:
            return f"{self.name}"
        return f"{self.entry1} at {self.exit1} - {self.entry2} at {self.exit2}"


class EmployeeShift(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    work_shift = models.ForeignKey(WorkShift, verbose_name=_("Work Shift"), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee} - {self.work_shift}"


class AttendanceHour(models.Model):
    hour = models.TimeField(verbose_name=_("Attendance Hour"))

    def __str__(self):
        return f"{self.hour}"


class AttendanceDay(models.Model):
    employee_shift = models.ForeignKey(EmployeeShift, verbose_name=_("Employee shift"), on_delete=models.CASCADE)
    day = models.DateField()
    attendance_hour = models.ManyToManyField(AttendanceHour, verbose_name=_("Hour registered"))
    worked_total = models.TimeField(default=datetime.min.time())

    def __str__(self):
        return f"{self.employee_shift.employee.get_full_name()} - {self.day}"

    def get_next_or_prev(self, models, item, direction):
        getit = False
        if direction == 'prev':
            models = models.reverse()
        for m in models:
            if getit:
                return m
            if item == m:
                getit = True
        if getit:
            # This would happen when the last
            # item made getit True
            return models[0]
        return False


class AttendanceMonth(models.Model):
    attendance_day = models.ManyToManyField(AttendanceDay, verbose_name=_("Attendance registered in day"))
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.CharField(max_length=2, choices=[(str(i), month_name[i]) for i in range(1, 13)], default=1)
    worked_total = models.IntegerField(verbose_name=_("Total worked month in seconds"), default=0)

    def __str__(self):
        return f"{self.employee.get_full_name()} - {month_name[int(self.month)]}"
