import time

from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone

from apps.pupil.models import Class, ClassSubject
from apps.schedule.models import ClassSchedule, ClassScheduleActivity
from apps.school.models import AcademicTerm
from apps.staff.models import Subject


def class_schedules(request, class_id, term_id):
    classe = Class.objects.get(id=class_id, school_id=request.user.school_id)
    term = AcademicTerm.objects.get(id=term_id, school_id=request.user.school_id)

    class_schedule = None
    schedule_subjects = None

    try:
        class_schedule = ClassSchedule.objects.get(classe=classe, academic_term=term, school_id=request.user.school_id)
        schedule_subjects = ClassScheduleActivity.objects.filter(class_schedule=class_schedule, school_id=request.user.school_id)
    except:pass

    days = [(0,'Mondays'), (1, 'Tuesdays'), (2, 'Wednesdays'), (3, 'Thursdays'), (4, 'Fridays')]

    hours = ['8:00', '9:00',
             '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'
             ]

    hours_list = []

    subjects = ClassSubject.objects.filter(school_id=request.user.school_id, classe=classe)
    for hour in hours:
        hours_list.append({'struct': time.strptime(hour, "%H:%M"), 'hours': hour})

    context = {
        'class': classe,
        'term': term,
        'days': days,
        'hours': hours,
        'subjects':subjects,
        'schedule': class_schedule,
        'schedule_activities': schedule_subjects,
        'errors': ''
    }

    if request.method == 'POST':
        print(request.POST)
        import re

        for data in request.POST:
            if re.search('[0-9]', data):
                data = data.split("-")
                day_hour = request.POST.get(f"{data[0]}-{data[1]}")

                try:
                    if re.search('[0-9]', day_hour):
                        csa = ClassScheduleActivity.objects.get(school_id=request.user.school_id,
                                                                day=data[0],
                                                                hour=data[1],
                                                                subject=Subject.objects.get(id=day_hour),
                                                                class_schedule__academic_term=term
                                                                )
                        context['errors'] = f"{csa.subject.description} is already scheduled for {csa.class_schedule.classe.description}"
                        return render(request, 'schedule/new_class.html', context)
                except ClassScheduleActivity.DoesNotExist:pass

        cs = ClassSchedule(
            classe=classe,
            academic_term=term,
            school_id=request.user.school_id,
            created_by=request.user
        )
        cs.save()

        for data in request.POST:
            if re.search('[0-9]', data):
                data = data.split("-")
                day_hour = request.POST.get(f"{data[0]}-{data[1]}")
                if re.search('[0-9]', day_hour):
                    ncsa = ClassScheduleActivity(
                        class_schedule=cs,
                        day=data[0],
                        hour=data[1],
                        subject=Subject.objects.get(id=day_hour),
                        is_subject=True,
                        # item=day_hour if not re.search('[0-9]', day_hour) else '',
                        school_id=request.user.school_id,
                        created_by=request.user
                    )

                    ncsa.save()
                else:
                    ncsa = ClassScheduleActivity(
                        class_schedule=cs,
                        day=data[0],
                        hour=data[1],
                        # subject=Subject.objects.get(id=day_hour),
                        # is_subject=True,
                        item=day_hour,
                        school_id=request.user.school_id,
                        created_by=request.user
                    )

                    ncsa.save()

        return redirect('schedule:class', class_id, term_id)

    return render(request, 'schedule/new_class.html', context)