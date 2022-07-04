from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from attendance.views import AttendanceMonthList


urlpatterns = [
    path('attedance-month/', AttendanceMonthList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
