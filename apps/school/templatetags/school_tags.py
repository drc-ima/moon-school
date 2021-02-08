from django import template
from datetime import date, timedelta, datetime
from apps.finance.models import FeeSchedule, FeeScheduleItem
from apps.pupil.models import *
from apps.schedule.models import ClassScheduleActivity
from apps.school.models import School, AcademicYear, AcademicTerm, PupilResult, PupilResultSubject, GradeScheme, \
    Attendance, PupilAttendance
from apps.staff.models import Subject, Staff

register = template.Library()


@register.simple_tag(takes_context=True)
def school(context):
    user = context['user']

    school_id = user.school_id
    sch = None
    try:
        sch = School.objects.get(school_id=school_id)
    except School.DoesNotExist:
        pass

    return sch


@register.simple_tag
def class_subjects(class_id):
    classe = Class.objects.get(id=class_id)

    cs = ClassSubject.objects.filter(classe=classe)

    return cs


@register.simple_tag
def subject_classes(subject_id):
    subject = Subject.objects.get(id=subject_id)

    sc = ClassSubject.objects.filter(subject=subject)

    return sc


@register.simple_tag
def session_terms(session_id):
    session = AcademicYear.objects.get(id=session_id)

    terms = AcademicTerm.objects.filter(academic_year=session)

    return terms


@register.simple_tag
def result_average(result_id):
    result = PupilResult.objects.get(id=result_id)

    subjects = PupilResultSubject.objects.filter(pupil_result=result)

    total_score = 0.0
    for subject in subjects:
        total_score += float(subject.total_score())

    avg = total_score / len(subjects)

    grade = GradeScheme.objects.get(from_score__lte=avg, to_score__gte=avg, school_id=result.school_id)

    return {
        'avg': round(avg, 2),
        'grade': grade.grade
    }


@register.simple_tag
def attendance_status(pupil_id, attendance_id):
    attendance = Attendance.objects.get(id=attendance_id)

    pupil = Pupil.objects.get(id=pupil_id)

    present = PupilAttendance.objects.filter(attendance=attendance, pupil=pupil, status=1, school_id=pupil.school_id).count()

    absent = PupilAttendance.objects.filter(attendance=attendance, pupil=pupil, status=0, school_id=pupil.school_id).count()

    total = PupilAttendance.objects.filter(attendance=attendance, pupil=pupil, school_id=pupil.school_id).count()

    return {
        'present': present,
        'absent': absent,
        'total': total,
        'attendances': PupilAttendance.objects.filter(attendance=attendance, pupil=pupil, school_id=pupil.school_id)
    }


@register.simple_tag
def fee_schedule_items(class_id, status, term):
    fee_schedule = None
    try:
        fee_schedule = FeeSchedule.objects.get(classe_id=class_id, student_status=status, academic_term_id=term)
    except:pass

    fsi = FeeScheduleItem.objects.filter(fee_schedule=fee_schedule)

    total_amount = 0

    # print(fee_schedule)

    # for fs in fsi:
    #     total_amount += fs.amount

    return {
        'items': fsi,
        'fs': fee_schedule
    }


@register.inclusion_tag('dashboards/head.html', takes_context=True)
def head_dashboard(context):
    user = context['user']

    school_id = user.school_id

    staffs = Staff.objects.filter(school_id=school_id).count()

    students = Pupil.objects.filter(school_id=school_id).count()
    term = None
    try:
        term = AcademicTerm.objects.get(is_current=True)
    except AcademicTerm.DoesNotExist:pass

    attendances = Attendance.objects.filter(school_id=school_id, academic_term=term).order_by('classs__description')
    
    classes = [attendance.classs.description for attendance in attendances]
    
    present = [PupilAttendance.objects.filter(attendance=attendance, status=1).count() for attendance in attendances]

    absent = [PupilAttendance.objects.filter(attendance=attendance, status=0).count() for attendance in attendances]

    return {
        'staffs':staffs,
        'students': students,
        'classes': classes,
        'present': present,
        'absent': absent,
    }


@register.inclusion_tag('dashboards/class_teacher.html', takes_context=True)
def ct_dashboard(context):
    user = context['user']

    school_id = user.school_id

    term, staff = None, None
    try:
        term = AcademicTerm.objects.get(is_current=True)
        staff = Staff.objects.get(school_id=school_id, user=user)
    except:
        pass

    my_subjects = Subject.objects.filter(teacher=staff, school_id=school_id)

    schedules = ClassScheduleActivity.objects.filter(
        subject__teacher=staff,
        class_schedule__academic_term=term,
        day=timezone.now().weekday()
    )

    today_week_number = datetime.today().weekday()
    twn_delta = timedelta(days=today_week_number)
    first_day = datetime.today() - twn_delta

    nav = [-1, 1]

    request = context['request']

    try:
        nav[0] = int(request.GET['n']) - 1
        nav[1] = int(request.GET['n']) + 1
        delta = timedelta(days=int(request.GET['n']) * 7)
        first_day = first_day + delta
    except:pass

    week = []
    labels = []
    present = []
    absent = []

    classe = Class.objects.get(teacher=staff)
    attendance = Attendance.objects.get(classs=classe, academic_term=term)
    pupils = Pupil.objects.filter(classs=classe, school_id=school_id)

    for i in range(5):
        delta = timedelta(days=i)
        week.append(({'number': datetime.date(first_day+delta).weekday(), 'day': datetime.strftime((first_day+delta), "%a"), 'date':  datetime.strftime((first_day+delta), "%Y-%m-%d")}))
        datte = datetime.strftime((first_day+delta), "%a")
        labels.append(datte)
        pa = PupilAttendance.objects.filter(attendance=attendance, date=datetime.strftime((first_day+delta), "%Y-%m-%d"))
        present.append(pa.filter(status=1).count())
        absent.append(pa.filter(status=0).count())

    return {
        'labels': labels,
        'present': present,
        'absent': absent,
        'week': week,
        'nav': nav,
        'schedules': schedules,
        'subjects': my_subjects,
        'students': pupils.count(),
        'class': classe
    }

