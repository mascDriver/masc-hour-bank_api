from dateutil.parser import isoparse
from dateutil.tz import tz
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from attendance.models import AttendanceMonth, AttendanceDay, AttendanceHour, EmployeeShift
from attendance.serializers import AttendanceMonthSerializer, AttendanceDaySerializer, RegisterSerializer, \
    MyTokenObtainPairSerializer


class AttendanceMonthViewset(ModelViewSet):
    permission_classes = (IsAuthenticated,)

    """
    List all AttendanceMonth, or create a new AttendanceMonth.
    """
    queryset = AttendanceMonth.objects.all()
    serializer_class = AttendanceMonthSerializer


class AttendanceMonthListApi(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            user_id = self.request.auth.payload.get('user_id')
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return AttendanceMonth.objects.filter(month=self.kwargs['month'], attendance_day__day__year=self.kwargs['year'],
                                              employee__id=user_id)

    serializer_class = AttendanceMonthSerializer


class AttendanceDayViewSet(ModelViewSet):
    """
    List all AttendanceMonth, or create a new AttendanceMonth.
    """
    permission_classes = (IsAuthenticated,)
    queryset = AttendanceDay.objects.all()
    serializer_class = AttendanceDaySerializer

    def destroy(self, request, *args, **kwargs):
        data = request.data
        object = self.get_object()
        try:
            object.attendance_hour.remove(AttendanceHour.objects.get(id=data['id']))
            object.save()
            serializer = AttendanceDaySerializer(object)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except:
            object.attendance_hour.clear()
            object.delete()
        return Response(status=status.HTTP_200_OK)


class AttendanceDayListApi(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            user_id = self.request.auth.payload.get('user_id')
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return AttendanceDay.objects.filter(day__month=self.kwargs['month'], day__year=self.kwargs['year'],
                                            day__day=self.kwargs['day'], employee_shift__employee__id=user_id)

    def create(self, request, *args, **kwargs):
        data = request.data
        day = isoparse(data.get('attendance_hour')).astimezone(tz.gettz('America/Sao_Paulo'))
        user_id = self.request.auth.payload.get('user_id')
        try:
            employee_shift = EmployeeShift.objects.get(employee=user_id)
        except EmployeeShift.DoesNotExist:
            employee_shift = EmployeeShift.objects.create(employee_id=user_id, work_shift_id=1)
        attendance_day, created = AttendanceDay.objects.get_or_create(day=day.date(), employee_shift=employee_shift)
        attendance_day.attendance_hour.add(AttendanceHour.objects.get(hour=day.replace(second=0, microsecond=0)))
        attendance_month, created = AttendanceMonth.objects.get_or_create(month=day.month, employee_id=user_id)
        if not attendance_month.attendance_day.filter(id=attendance_day.id).exists():
            attendance_month.attendance_day.add(attendance_day)
        serializer = AttendanceDaySerializer(attendance_day)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    serializer_class = AttendanceDaySerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class TokenViewBaseCustom(TokenViewBase):
    def post(self, request, *args, **kwargs):
        response = super(TokenViewBaseCustom, self).post(request, *args, **kwargs)
        authenticate(username=request.data['username'], password=request.data['password'])
        return response


class MyTokenObtainPairView(TokenViewBaseCustom):
    serializer_class = MyTokenObtainPairSerializer


def logout_api(request):
    logout(request)
    return HttpResponse()