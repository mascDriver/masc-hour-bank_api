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
        fields = '__all__'


class AttendanceDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceDay
        fields = ('employee_shift', 'day', 'attendance_hour', 'worked_total')

    def to_representation(self, instance):
        representation = super(AttendanceDaySerializer, self).to_representation(instance)
        representation['attendance_hour'] = AttendanceHourSerializer(instance.attendance_hour.all(), many=True).data
        representation['employee_shift'] = EmployeeShiftSerializer(instance.employee_shift).data
        return representation


class AttendanceMonthSerializer(serializers.ModelSerializer):
    attendance_day = AttendanceDaySerializer(many=True)

    class Meta:
        model = AttendanceMonth
        fields = '__all__'