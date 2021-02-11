import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from django.utils.text import slugify

from apps.account.models import User
from apps.pupil.models import ClassSubject, Class, Pupil
from apps.schedule.models import ClassScheduleActivity
from apps.school.models import School, AcademicYear, AcademicTerm, Result, PupilResult, PupilResultSubject, GradeScheme, \
    Attendance, PupilAttendance
from apps.staff import forms
from apps.staff.models import Staff, Subject
from utils.randoms import account_id, institution_id
from utils.decorators import *


@login_required()
@school_admin_required
def staffs(request):
    staff = Staff.objects.filter(school_id=request.user.school_id)

    head = None
    try:
        head = User.objects.get(user_type='SH', school_id=request.user.school_id)
    except User.DoesNotExist:
        pass

    context = {
        'object_list': staff,
        'head': head,
        'errors': ''
    }

    if request.method == 'POST':
        form = request.POST.get('form')

        if form == 'head':
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            mname = request.POST.get('middle_name')
            email = request.POST.get('email')

            try:
                User.objects.get(username=email, school_id=request.user.school_id)
                context['errors'] = 'This email already exist'
                return render(request, 'staff/index.html', context)
            except User.DoesNotExist:pass

            uc = User.objects.filter(school_id=request.user.school_id).count() + 1

            uc = '{0:04}'.format(uc)

            inst = School.objects.get(school_id=request.user.school_id)

            user = User(
                username=email,
                email=email,
                first_name=fname,
                middle_name=mname,
                last_name=lname,
                slug="-".join((slugify(fname), slugify(lname))),
                user_type='SH',
                account_id=account_id(inst.name, fname, lname, uc),
                school_id=request.user.school_id
            )

            user.set_password('password')

            mystaff = Staff(
                staff_type='SH',
                first_name=fname,
                middle_name=mname,
                last_name=lname,
                created_by=request.user,
                slug="-".join((slugify(fname), slugify(lname))),
                account_activated=True,
                school_id=request.user.school_id,
            )

            user.save()
            mystaff.save()

            return redirect('staff:list')
        elif form == 'activate':
            staff_id = request.POST.get('staff')

            staff_obj = Staff.objects.get(id=staff_id)
            email = request.POST.get('email')

            try:
                User.objects.get(username=email, school_id=staff_obj.school_id)
                context['errors'] = 'This email already exist'
                return render(request, 'staff/index.html', context)
            except User.DoesNotExist:pass

            uc = User.objects.filter(school_id=request.user.school_id).count() + 1

            uc = '{0:04}'.format(uc)

            inst = School.objects.get(school_id=request.user.school_id)

            user = User(
                username=email,
                email=email,
                first_name=staff_obj.first_name,
                middle_name=staff_obj.middle_name,
                last_name=staff_obj.last_name,
                slug="-".join((slugify(staff_obj.first_name), slugify(staff_obj.last_name))),
                user_type=staff_obj.staff_type,
                account_id=account_id(inst.name, staff_obj.first_name, staff_obj.last_name, uc),
                school_id=request.user.school_id,
                profile=staff_obj.profile
            )

            user.set_password('password')

            staff_obj.account_activated = True

            user.save()

            staff_obj.user = user

            staff_obj.save()

            return redirect('staff:list')

    return render(request, 'staff/index.html', context)


@login_required()
@school_head_required
def new_staff(request):
    context = {
        'form': forms.StaffForm
    }

    if request.method == 'POST':
        form = forms.StaffForm(request.POST)
        profile = request.FILES.get('profile')

        if form.is_valid():
            form.instance.slug = "-".join((slugify(form.instance.first_name), slugify(form.instance.last_name)))
            form.instance.school_id = request.user.school_id
            form.instance.created_by = request.user
            form.instance.profile = profile
            form.save()

            return redirect('staff:list')

    return render(request, 'staff/add.html', context)


@login_required()
@teacher_required
def mysubjects(request):

    staff = None

    try:
        staff = Staff.objects.get(school_id=request.user.school_id, user=request.user)
    except Staff.DoesNotExist:pass

    subjects = Subject.objects.filter(school_id=request.user.school_id, teacher=staff)

    context = {
        'object_list': subjects
    }

    return render(request, 'staff/mysubjects.html', context)


@login_required()
@teacher_required
def subject_class(request, subject_id, class_id):
    subject = Subject.objects.get(school_id=request.user.school_id, id=subject_id)

    classe = Class.objects.get(id=class_id, school_id=request.user.school_id)

    sessions = AcademicYear.objects.filter(school_id=request.user.school_id)

    context = {
        'object': classe,
        'subject': subject,
        'sessions': sessions
    }

    return render(request, 'staff/subject_class.html', context)


@login_required()
@teacher_required
def subject_class_term(request, subject_id, class_id, term_id):
    subject = Subject.objects.get(school_id=request.user.school_id, id=subject_id)

    classe = Class.objects.get(id=class_id, school_id=request.user.school_id)

    term = AcademicTerm.objects.get(school_id=request.user.school_id, id=term_id)

    result = None

    try:
        result = Result.objects.get(academic_term=term, status=0, school_id=request.user.school_id)
    except Result.DoesNotExist:pass

    pupils = PupilResult.objects.filter(classe=classe, school_id=request.user.school_id, result=result)

    prs = PupilResultSubject.objects.filter(school_id=request.user.school_id, subject=subject, result=result)

    context = {
        'object': term,
        'subject': subject,
        'class': classe,
        'pupils': pupils,
        'result': result,
        'prs': prs,
        'errors': ''
    }

    if request.method == 'POST':
        # print(request.POST)
        form = request.POST.get('form')

        if form == 'score':
            class_score = request.POST.getlist('class_score')
            exam_score = request.POST.getlist('exam_score')
            pupil = request.POST.getlist('pupil')

            for pup in range(len(pupil)):
                try:
                    pup_obj = Pupil.objects.get(id=pupil[pup])
                    pup_class = class_score[pup]
                    pup_exam = exam_score[pup]
                    if (float(pup_class) + float(pup_exam)) > 100.0:
                        context['errors'] = f"Class score ({pup_class}) and exams score ({pup_exam}) for {pup_obj.full_name()} is more than 100%"
                        return render(request, 'staff/subject_class_term.html', context)
                    # print(pup_obj.full_name() + ' Class: ' + class_score[pup] + ' Exams: ' + exam_score[pup])

                    score = pup_class + pup_exam
                    try:
                        GradeScheme.objects.get(from_score__lte=score, to_score__gte=score,
                                                    school_id=request.user.school_id)
                    except GradeScheme.DoesNotExist:
                        context['errors'] = 'Score is out of grade scheme'
                        return render(request, 'staff/subject_class_term.html', context)
                except:pass

            for pup in range(len(pupil)):
                try:
                    pup_obj = Pupil.objects.get(id=pupil[pup], school_id=request.user.school_id)
                    pup_class = float(class_score[pup])
                    pup_exam = float(exam_score[pup])
                    pupil_result = PupilResult.objects.get(result=result, classe=classe, pupil=pup_obj, school_id=request.user.school_id)
                    score = pup_class + pup_exam
                    grade = GradeScheme.objects.get(from_score__lte=score, to_score__gte=score, school_id=request.user.school_id)

                    nprs = PupilResultSubject(
                        subject=subject,
                        pupil_result=pupil_result,
                        result=result,
                        class_score=pup_class,
                        exam_score=pup_exam,
                        pupil=pup_obj,
                        grade=grade.grade,
                        created_by=request.user,
                        school_id=request.user.school_id
                    )

                    nprs.save()
                    # return redirect('staff:subject-class-term', subject_id, class_id, term_id)
                except:pass

            # for data in request.POST:
            #     print(data)
            #     class_score = request.POST.get(data if data == 'class_score' else None)
            #     print(class_score)
            # for pupil in range(len(pupils)):
            #
            #     # class_score = class_score[pupil]
            #     # exam_score = exam_score[pupil]
            #     print(str(pupil) + ' = ' + 'Class ' + class_score[pupil] + ' Exams ' + exam_score[pupil])

            # for data in request.POST:
            #     if re.search('[0-9]', data):
            #         data = data.split("-")
            #         # print(data)
            #         if data[1] == 'class_score':
            #             class_score = request.POST.get(f"{data[0]}-{data[1]}")
            #             # request.session['class_score'] = None
            #             request.session[f"{data[0]}-class_score"] = class_score
            #             pupil = None
            #             # print(class_score)
            #             try:
            #                 pupil = Pupil.objects.get(id=data[0], school_id=request.user.school_id)
            #                 #print('Class score for ' + pupil.full_name() + ' ' + class_score)
            #             except:pass
            #                 #print('Error class')
            #
            # for data in request.POST:
            #     if re.search('[0-9]', data):
            #         data = data.split("-")
            #         exam_score = request.POST.get(f"{data[0]}-{data[1]}") if data[1] == 'exam_score' else 0.0
            #         class_score = request.POST.get(f"{data[0]}-{data[1]}") if data[1] == 'class_score' else 0.0
            #         if data[1] == 'class_score':
            #             pass
            #             # class_score = request.session[f"{data[0]}-class_score"]
            #             # try:
            #             #     pupil = Pupil.objects.get(id=data[0], school_id=request.user.school_id)
            #             #     print('Pupil: '+ pupil.full_name() + ' Exams: ' + exam_score + ' Class: ' + class_score)
            #             #     score = float(exam_score) + float(class_score)
            #             #     if score > 100.0:
            #             #         context['errors'] = f"Class {class_score} and exams {exam_score} score recorded for {pupil.full_name()} is more than 100 percent"
            #             #         return render(request, 'staff/subject_class_term.html', context)
            #             #     # class_score = request.session['class_score']
            #             #     #print('Exam score ' + pupil.full_name() + ' ' + exam_score)
            #             #     # score = float(exam_score) + float(class_score)
            #             #     # print(class_score)
            #             #
            #             #     # request.session['class_score'] = None
            #             # except Pupil.DoesNotExist:pass
            #                 #print('error exams')
            #         elif data[1] == 'exam_score':
            #
            #             try:
            #                 pupil = Pupil.objects.get(id=data[0])
            #                 print(f'{pupil.full_name()} Class: {class_score} Exams: {exam_score}')
            #             except Pupil.DoesNotExist:pass

            return redirect('staff:subject-class-term', subject_id, class_id, term_id)
            # return render(request, 'staff/subject_class_term.html', context)
        elif form == 'edit':
            class_score = request.POST.get('eclass_score')
            exam_score = request.POST.get('eexam_score')
            pupil_id = request.POST.get('epupil')

            pupil = Pupil.objects.get(id=pupil_id)

            if (float(class_score) + float(exam_score)) > 100.0:
                context[
                    'errors'] = f"Class score ({classe}) and exams score ({exam_score}) for {pupil.full_name()} is more than 100%"
                return render(request, 'staff/subject_class_term.html', context)
            score = float(class_score) + float(exam_score)
            grade = None
            try:
                grade = GradeScheme.objects.get(from_score__lte=score, to_score__gte=score,
                                            school_id=request.user.school_id)
            except GradeScheme.DoesNotExist:
                context['errors'] = 'Score is out of grade scheme'
                return render(request, 'staff/subject_class_term.html', context)

            pupil_result = PupilResult.objects.get(result=result, classe=classe, pupil=pupil,
                                                   school_id=request.user.school_id)
            pupil_subject_result = PupilResultSubject.objects.get(subject=subject, pupil_result=pupil_result, result=result, pupil=pupil)

            pupil_subject_result.class_score = class_score
            pupil_subject_result.exam_score = exam_score
            pupil_subject_result.grade = grade.grade
            pupil_subject_result.save()

            return redirect('staff:subject-class-term', subject_id, class_id, term_id)
    return render(request, 'staff/subject_class_term.html', context)


@login_required()
@class_teacher_required
def class_attendance(request):
    today = datetime.datetime.strptime(request.GET.get('today'), '%Y-%m-%d').date() if request.GET.get(
        'today') else timezone.now().date()
    ndate = today + datetime.timedelta(days=1)

    pdate = today - datetime.timedelta(days=1)

    ndate = datetime.datetime.strftime(ndate, '%Y-%m-%d')

    pdate = datetime.datetime.strftime(pdate, '%Y-%m-%d')

    attendance = None
    classe = None
    current_term = None

    try:
        current_term = AcademicTerm.objects.get(is_current=True, school_id=request.user.school_id)
        staff = Staff.objects.get(user=request.user, school_id=request.user.school_id)
        classe = Class.objects.get(teacher=staff, school_id=request.user.school_id)
        attendance = Attendance.objects.get(classs=classe, academic_term=current_term, school_id=request.user.school_id)
    except:pass

    pupil_attendance = PupilAttendance.objects.filter(attendance=attendance, date__day=today.day, date__month=today.month, date__year=today.year)

    pupils = Pupil.objects.filter(classs=classe, school_id=request.user.school_id)

    context = {
        'pdate': pdate,
        'ndate': ndate,
        'today': today,
        'attendance': attendance,
        'classe': classe,
        'pupil_attendance': pupil_attendance,
        'term': current_term,
        'pupils': pupils
    }

    if request.method == 'POST':

        form = request.POST.get('form')
        days = current_term.end_date - current_term.start_date
        if form == 'init':
            attn = Attendance(
                academic_term=current_term,
                academic_year=current_term.academic_year,
                classs=classe,
                created_by=request.user,
                school_id=request.user.school_id,
                number_of_days=days.days
            )

            attn.save()

            return redirect('staff:class-attendance')
        elif form == 'mark':
            pupil = request.POST.getlist('pupil')
            status = request.POST.getlist('status')

            for pup in range(len(pupil)):
                try:
                    pup_obj = Pupil.objects.get(id=pupil[pup])
                    atd_status = status[pup]

                    natd = PupilAttendance(
                        attendance=attendance,
                        date=today,
                        pupil=pup_obj,
                        status=atd_status,
                        created_by=request.user,
                        school_id=request.user.school_id
                    )

                    natd.save()
                except:pass

            return redirect('staff:class-attendance')

    return render(request, 'staff/class_attendance.html', context)


@login_required()
@teacher_required
def myschedules(request):

    teacher = None
    current_term = None
    schedules = None
    try:
        current_term = AcademicTerm.objects.get(is_current=True)
    except:pass

    try:
        teacher = Staff.objects.get(user=request.user, school_id=request.user.school_id)
        schedules = ClassScheduleActivity.objects.filter(
            subject__teacher=teacher,
            class_schedule__academic_term=current_term
        )
    except:pass

    days = [(0, 'Mondays'), (1, 'Tuesdays'), (2, 'Wednesdays'), (3, 'Thursdays'), (4, 'Fridays')]

    hours = ['8:00', '9:00',
             '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'
             ]

    context = {
        'object_list': schedules,
        'term': current_term,
        'days': days,
        'hours': hours
    }

    return render(request, 'staff/myschedules.html', context)
