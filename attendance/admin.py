from django.contrib import admin

from attendance.models import AttendanceDay, AttendanceMonth, EmployeeShift, WorkShift


class BatidaPontoInline(admin.StackedInline):
    extra = 0
    model = AttendanceDay.attendance_hour.through


@admin.register(AttendanceDay)
class RelogioPontoAdmin(admin.ModelAdmin):
    inlines = (BatidaPontoInline,)
    filter_horizontal = ('attendance_hour',)
    fields = ('employee_shift', 'day', 'worked_total', 'attendance_hour')
    autocomplete_fields = ('employee_shift', )
    search_fields = ('employee_shift__id', 'employee_shift__username', 'employee_shift__first_name')
    list_filter = ('day',)


class RelogioPontoInline(admin.TabularInline):
    model = AttendanceMonth.attendance_day.through
    extra = 0


@admin.register(AttendanceMonth)
class RelogioPontoMesAdmin(admin.ModelAdmin):
    inlines = (RelogioPontoInline,)
    fields = ('employee', 'month', 'worked_total')
    autocomplete_fields = ('employee', )


@admin.register(WorkShift)
class TurnoAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeShift)
class FuncionarioTurnoAdmin(admin.ModelAdmin):
    search_fields = ('employee',)
