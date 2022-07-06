from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from attendance.models import AttendanceMonth
from attendance.serializers import AttendanceMonthSerializer


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