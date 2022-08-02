from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from attendance.models import AttendanceMonth, AttendanceDay, AttendanceHour
from attendance.serializers import AttendanceMonthSerializer, AttendanceDaySerializer
from dateutil.parser import parse

class AttendanceMonthViewset(ModelViewSet):
    """
    List all AttendanceMonth, or create a new AttendanceMonth.
    """
    queryset = AttendanceMonth.objects.all()
    serializer_class = AttendanceMonthSerializer


class AttendanceMonthListApi(ListCreateAPIView):
    def get_queryset(self):
        return AttendanceMonth.objects.filter(month=self.kwargs['month'], attendance_day__day__year=self.kwargs['year'])

    serializer_class = AttendanceMonthSerializer


class AttendanceDayViewSet(ModelViewSet):
    """
    List all AttendanceMonth, or create a new AttendanceMonth.
    """
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
    def get_queryset(self):
        return AttendanceDay.objects.filter(day__month=self.kwargs['month'], day__year=self.kwargs['year'],
                                            day__day=self.kwargs['day'])

    def create(self, request, *args, **kwargs):
        data = request.data
        day = parse(data.get('attendance_hour'))
        attendance_day, created = AttendanceDay.objects.get_or_create(day=day.utcnow().date(), employee_shift_id=1)
        attendance_day.attendance_hour.add(AttendanceHour.objects.get(hour=day.replace(second=0, microsecond=0)))
        serializer = AttendanceDaySerializer(attendance_day)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    serializer_class = AttendanceDaySerializer
