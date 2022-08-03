from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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
        if not instance.attendance_hour.filter(hour=data['attendance_hour']).exists():
            instance.attendance_hour.remove(AttendanceHour.objects.get(id=data['id']))
        instance.attendance_hour.add(AttendanceHour.objects.get(hour=data['attendance_hour']))
        return instance

    class Meta:
        model = AttendanceDay
        fields = '__all__'


class AttendanceMonthSerializer(serializers.ModelSerializer):
    attendance_day = AttendanceDaySerializer(many=True)

    class Meta:
        model = AttendanceMonth
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user