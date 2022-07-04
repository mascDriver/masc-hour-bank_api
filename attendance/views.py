from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import AttendanceMonth
from attendance.serializers import AttendanceMonthSerializer


class AttendanceMonthList(APIView):
    def get(self, request, format=None):
        attendance_month = AttendanceMonth.objects.all()
        serializer = AttendanceMonthSerializer(attendance_month, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
