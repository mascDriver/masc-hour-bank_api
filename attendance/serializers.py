from rest_framework import serializers

from attendance.models import AttendanceMonth, AttendanceDay, AttendanceHour, EmployeeShift


class EmployeeShiftSerializer(serializers.ModelSerializer):
    work_shift = serializers.StringRelatedField()
    employee = serializers.StringRelatedField()

    class Meta:
        model = EmployeeShift
        fields = ('employee', 'work_shift')


class AttendanceHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceHour
        fields = ('hour', )


class AttendanceDaySerializer(serializers.ModelSerializer):
    attendance_hour = AttendanceHourSerializer(many=True)
    employee_shift = EmployeeShiftSerializer()

    class Meta:
        model = AttendanceDay
        fields = '__all__'



class AttendanceMonthSerializer(serializers.ModelSerializer):
    attendance_day = AttendanceDaySerializer(many=True)

    class Meta:
        model = AttendanceMonth
        fields = '__all__'