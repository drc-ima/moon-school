from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from apps.pupil.models import Class, Pupil, ClassSubject
from apps.school.models import AcademicYear, AcademicTerm, Result, PupilResult, PupilResultSubject, Attendance, \
    PupilAttendance
from apps.staff.models import Staff


@login_required()
def myclass(request):
    staff = Staff.objects.get(user=request.user, school_id=request.user.school_id)
    my_class = Class.objects.get(teacher=staff, school_id=request.user.school_id)
    pupils = Pupil.objects.filter(classs=my_class, school_id=request.user.school_id)
    class_subjects = ClassSubject.objects.filter(school_id=request.user.school_id, classe=my_class)

    sessions = AcademicYear.objects.filter(school_id=request.user.school_id)

    context = {
        'object': my_class,
        'pupils': pupils,
        'subjects': class_subjects,
        'sessions': sessions
    }

    return render(request, 'pupil/myclass.html', context)


@login_required()
def class_term_results(request, term_id, class_id):
    term = AcademicTerm.objects.get(id=term_id, school_id=request.user.school_id)
    classe = Class.objects.get(id=class_id, school_id=request.user.school_id)

    pupils = Pupil.objects.filter(school_id=request.user.school_id, classs=classe)

    result = None
    try:
        result = Result.objects.get(school_id=request.user.school_id, academic_term=term)
    except Result.DoesNotExist:pass

    results = PupilResult.objects.filter(result=result, classe=classe, school_id=request.user.school_id)

    context = {
        'object': term,
        'class': classe,
        'pupils': pupils,
        'result': result,
        'results': results,
    }

    try:
        open_all = request.GET.get('open')
        if open_all == 'YES':
            for pupil in pupils:
                npr = PupilResult(
                    result=result,
                    classe=classe,
                    pupil=pupil,
                    status=0,
                    created_by=request.user,
                    school_id=request.user.school_id
                )

                npr.save()
                # print(pupil)

            return redirect('pupil:class_term', class_id, term_id)

    except:pass

    return render(request, 'pupil/class_term.html', context)


@login_required()
def class_term_attendance(request, term_id, class_id):
    term = AcademicTerm.objects.get(id=term_id, school_id=request.user.school_id)
    classe = Class.objects.get(id=class_id, school_id=request.user.school_id)

    pupils = Pupil.objects.filter(classs=classe, school_id=request.user.school_id)

    attendance = None

    try:
        attendance = Attendance.objects.get(academic_term=term, school_id=request.user.school_id)
    except Attendance.DoesNotExist:pass

    context = {
        'object': term,
        'class': classe,
        'pupils': pupils,
        'attendance': attendance,
    }

    return render(request, 'pupil/class_term_attendance.html', context)


@login_required()
def class_term_attendance_pupil(request, attendance_id, pupil_id):
    attendance = Attendance.objects.get(id=attendance_id, school_id=request.user.school_id)
    pupil = Pupil.objects.get(id=pupil_id, school_id=request.user.school_id)
    pupil_attendance = PupilAttendance.objects.filter(attendance=attendance, pupil=pupil, school_id=request.user.school_id)

    context = {
        'object': attendance,
        'attendances': pupil_attendance,
        'pupil': pupil
    }

    return render(request, 'pupil/class_term_attendance_pupil.html', context)


@login_required()
def class_term_pupil(request, pupil_result_id):
    pupil_result = PupilResult.objects.get(id=pupil_result_id, school_id=request.user.school_id)

    pupil_result_subjects = PupilResultSubject.objects.filter(pupil_result=pupil_result, school_id=request.user.school_id)

    context = {
        'object': pupil_result,
        'subjects': pupil_result_subjects
    }

    return render(request, 'pupil/class_term_pupil.html', context)