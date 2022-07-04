from rest_framework import serializers

from attendance.models import AttendanceMonth


class AttendanceMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceMonth
        fields = '__all__'