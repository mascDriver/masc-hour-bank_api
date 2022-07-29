from django.urls import path, include
from rest_framework import routers

from attendance.views import *

router = routers.DefaultRouter()
router.register('month', AttendanceMonthViewset, basename='month')
router.register('day', AttendanceDayViewSet, basename='day')

urlpatterns = [
    path('', include(router.urls)),
    path('month/<int:month>/year/<int:year>', AttendanceMonthListApi.as_view()),
    path('day/<int:day>/month/<int:month>/year/<int:year>', AttendanceDayListApi.as_view())
]
