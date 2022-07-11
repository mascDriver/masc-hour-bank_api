from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from attendance.models import AttendanceMonth, AttendanceDay
from attendance.serializers import AttendanceMonthSerializer, AttendanceDaySerializer


class AttendanceMonthList(ListCreateAPIView):
    """
    List all AttendanceMonth, or create a new AttendanceMonth.
    """
    queryset = AttendanceMonth.objects.all()
    serializer_class = AttendanceMonthSerializer


class AttendanceMonthDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a AttendanceMonth instance.
    """
    queryset = AttendanceMonth.objects.all()
    serializer_class = AttendanceMonthSerializer


class AttendanceDayList(ListCreateAPIView):
    """
    List all AttendanceMonth, or create a new AttendanceMonth.
    """
    queryset = AttendanceDay.objects.all()
    serializer_class = AttendanceDaySerializer


class AttendanceDayDetail(RetrieveUpdateDestroyAPIView):
    """
    List all AttendanceMonth, or create a new AttendanceMonth.
    """
    queryset = AttendanceDay.objects.all()
    serializer_class = AttendanceDaySerializer
