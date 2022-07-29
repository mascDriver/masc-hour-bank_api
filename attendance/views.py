from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from attendance.models import AttendanceMonth, AttendanceDay
from attendance.serializers import AttendanceMonthSerializer, AttendanceDaySerializer


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


class AttendanceDayListApi(ListCreateAPIView):
    def get_queryset(self):
        return AttendanceDay.objects.filter(day__month=self.kwargs['month'], day__year=self.kwargs['year'],
                                            day__day=self.kwargs['day'])

    serializer_class = AttendanceDaySerializer
