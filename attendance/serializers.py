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
    attendance_hour = AttendanceHourSerializer(many=True, read_only=True)
    employee_shift = serializers.StringRelatedField(read_only=True)
    day = serializers.DateField(read_only=True)

    def update(self, instance, validated_data):
        data = self.context['request'].data
        instance.attendance_hour.add(AttendanceHour.objects.get(hour=data['attendance_hour']))
        instance.attendance_hour.remove(AttendanceHour.objects.get(id=data['id']))
        return instance

    class Meta:
        model = AttendanceDay
        fields = '__all__'


class AttendanceMonthSerializer(serializers.ModelSerializer):
    attendance_day = AttendanceDaySerializer(many=True)

    class Meta:
        model = AttendanceMonth
        fields = '__all__'