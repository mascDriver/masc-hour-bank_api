from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from attendance.views import AttendanceMonthList, AttendanceMonthDetail


urlpatterns = [
    path('attedance-month/', AttendanceMonthList.as_view()),
    path('attedance-month/<int:pk>', AttendanceMonthDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
