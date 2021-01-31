from django import template

from apps.finance.models import FeeSchedule, FeeScheduleItem
from apps.pupil.models import *
from apps.school.models import School, AcademicYear, AcademicTerm, PupilResult, PupilResultSubject, GradeScheme, \
    Attendance, PupilAttendance
from apps.staff.models import Subject

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
        'avg': avg,
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