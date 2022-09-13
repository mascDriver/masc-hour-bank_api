import calendar
from datetime import datetime, date

from apscheduler.schedulers.background import BackgroundScheduler
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, AndroidConfig, AndroidNotification

from attendance.models import WorkShift, EmployeeShift

message = Message(
    data={
        "title": "Atenção!",
        "body": "Está na hora de bater o ponto ⌚⌚⌚",
        "data": '{"click_action": "/day"}',
        "priority": "high"
    },
    android=AndroidConfig(
        notification=AndroidNotification(
            icon="https://hourbank.mascdriver.com.br/badge_128.png",
            title="Atenção!",
            body="Está na hora de bater o ponto ⌚⌚⌚",
        )
    )
)



def verify_not_entrys():
    """
    Verifica se um employee nao teve a entrada marcada no horario de seu workshift
    :return: obj
    :rtype:
    """
    business_week = ((0, calendar.day_abbr[0:5]), (1, calendar.day_abbr[0:6]))
    for work_shift in WorkShift.objects.all():
        employee_shift = EmployeeShift.objects.filter(work_shift=work_shift)
        if calendar.day_abbr[date.today().weekday()] in business_week[int(work_shift.working_days)][1]:
            if datetime.now().time().replace(microsecond=0, second=0) in (
                    work_shift.entry1, work_shift.entry2, work_shift.exit1, work_shift.exit2):
                for employee_shift in employee_shift:
                    FCMDevice.objects.filter(user=employee_shift.employee).send_message(message)


scheduler = BackgroundScheduler()
scheduler.add_job(verify_not_entrys, 'cron', minute='*')
scheduler.start()
