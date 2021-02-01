import datetime
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.text import slugify
from rest_framework.status import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.models import User
from apps.account.serializers import UserSerializer
from apps.pupil.models import Class, ClassSubject, Pupil, PupilClass
from apps.schedule.models import ClassSchedule
from apps.school import forms
from apps.school.models import GradeScheme, AcademicYear, AcademicTerm, Attendance, PupilResult, Result
from apps.school.serializers import *
from apps.staff.models import Subject, Staff, SubjectTeacher
from utils.randoms import *

# deprecated
class SchoolSignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        first_name = request.data.get('first_name', None)
        middle_name = request.data.get('middle_name', None)
        last_name = request.data.get('last_name', None)
        password = request.data.get('password', None)
        name = request.data.get('institution', None)
        logo = request.data.get('logo', None)
        phone_number = request.data.get('phone_number', None)
        domain = request.data.get('domain', None)
        gps = request.data.get('gps', None)

        try:
            User.objects.get(username=email)
            return Response({'detail': 'Email already exist'}, status=HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass


        try:
            School.objects.get(domain=domain)
            return Response({'detail': "There's already a school with this domain registered"}, status=HTTP_400_BAD_REQUEST)
        except School.DoesNotExist:
            pass

        inst_count = School.objects.count()

        inst_count = '{0:04}'.format(inst_count)

        user_count = User.objects.filter(school_id=institution_id(name, inst_count)).count()

        user_count = '{0:04}'.format(user_count)

        user = User(
            username=email,
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            slug="-".join((slugify(first_name), slugify(last_name))),
            user_type='SAD',
            account_id=account_id(name, first_name, last_name, user_count),
            school_id=institution_id(name, inst_count),
        )

        user.set_password(password)

        school = School(
            name=name,
            logo=logo,
            gps_address=gps,
            phone_number=phone_number,
            slug=slugify(name),
            created_by=user,
            domain=domain,
            school_id=institution_id(name, inst_count),
        )

        user.save()
        school.save()

        user = UserSerializer(user, context={'request': request})

        school = SchoolSerializer(school, context={'request': request})

        return Response(
            {
                'user': user.data,
                'institution': school.data
            },
            status=HTTP_201_CREATED
        )


@login_required()
def myschool(request):
    school = School.objects.get(school_id=request.user.school_id)
    context = {
        'object': school
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        phone_number = request.POST.get('phone')

        school.name = name

        if request.FILES.get('logo'):
            school.logo = logo

        school.phone_number = phone_number

        school.save()

        return redirect('school:myschool')

    return render(request, 'school/myschool.html', context)



@login_required()
def management(request):
    context = {
        'classes': Class.objects.filter(school_id=request.user.school_id),
        'subjects': Subject.objects.filter(school_id=request.user.school_id),
        'grades': GradeScheme.objects.filter(school_id=request.user.school_id),
        'errors': '',
    }

    if request.method == 'POST':
        form = request.POST.get('form')
        if form == 'class':
            desc = request.POST.get('description')

            Class.objects.create(
                description=desc,
                created_by=request.user,
                school_id=request.user.school_id
            )

            return redirect('school:management')

        elif form == 'subject':
            desc = request.POST.get('description')
            code = request.POST.get('code')

            Subject.objects.create(
                description=desc,
                subject_code=code,
                created_by=request.user,
                school_id=request.user.school_id
            )

            return redirect('school:management')

        elif form == 'grade':
            from_score = request.POST.get('from_score')
            to_score = request.POST.get('to_score')
            grade = request.POST.get('grade')

            try:
                GradeScheme.objects.get(school_id=request.user.school_id, from_score__lte=from_score, to_score__gte=to_score)
                context['errors'] = 'Grade range invalid'
                return render(request, 'school/management.html', context)
            except GradeScheme.DoesNotExist:
                pass

            gs = GradeScheme(
                from_score=from_score,
                to_score=to_score,
                grade=grade,
                school_id=request.user.school_id,
                created_by=request.user
            )

            gs.save()

            return redirect('school:management')
        elif form == 'remgrade':
            grade_id = request.POST.get('grade')

            grade = GradeScheme.objects.get(school_id=request.user.school_id, id=grade_id)

            grade.delete()

            return redirect('school:management')
    return render(request, 'school/management.html', context)


@login_required()
def class_detail(request, id):
    classe = Class.objects.get(id=id, school_id=request.user.school_id)

    subjects = ClassSubject.objects.filter(school_id=request.user.school_id, classe=classe)
    subs = Subject.objects.filter(school_id=request.user.school_id)
    students = Pupil.objects.filter(school_id=request.user.school_id, classs=classe)
    context = {
        'object': classe,
        'subjects': subjects,
        'subs':subs,
        'errors': '',
        'students': students,
        'class_teachers': Staff.objects.filter(school_id=request.user.school_id, staff_type='CT')
    }

    if request.method == 'POST':
        form = request.POST.get('form')

        if form == 'subject':
            subject_id = request.POST.get('subject')

            try:
                ClassSubject.objects.get(school_id=request.user.school_id, subject_id=subject_id, classe=classe)
                context['errors'] = 'This subject is already scheduled for this class'
                return render(request, 'school/class.html', context)
            except ClassSubject.DoesNotExist:pass

            ClassSubject.objects.create(
                classe=classe,
                subject_id=subject_id,
                school_id=request.user.school_id,
                created_by=request.user
            )

            return redirect('school:management-class', id)

        elif form == 'remsub':
            sub_id = request.POST.get('sub')
            sub = ClassSubject.objects.get(id=sub_id, school_id=request.user.school_id)

            sub.delete()

            return redirect('school:management-class', id)

        elif form == 'assign':
            teach_id = request.POST.get('teacher')
            teacher = Staff.objects.get(id=teach_id)

            try:
                cls = Class.objects.get(teacher=teacher)
                context['errors'] = f'This teacher has already been assigned to {cls.description}'
                return render(request, 'school/class.html', context)
            except Class.DoesNotExist:
                pass

            classe.teacher = teacher

            classe.save()

            return redirect('school:management-class', id)

        elif form == 'remteach':
            classe.teacher = None

            classe.save()

            return redirect('school:management-class', id)
    return render(request, 'school/class.html', context)


@login_required()
def subject_detail(request, id):
    subject = Subject.objects.get(id=id, school_id=request.user.school_id)

    classes = ClassSubject.objects.filter(subject=subject, school_id=request.user.school_id)

    teachers = SubjectTeacher.objects.filter(subject=subject, school_id=request.user.school_id)

    context = {
        'object': subject,
        'classes': classes,
        'teachers': teachers,
        'errors': '',
        'all_teachers': Staff.objects.filter(school_id=request.user.school_id).filter(Q(staff_type='CT') | Q(staff_type='TU'))
    }

    if request.method == 'POST':
        form = request.POST.get('form')

        if form == 'teacher':
            teach_id = request.POST.get('teacher')

            teacher = Staff.objects.get(school_id=request.user.school_id, id=teach_id)

            # try:
            if subject.teacher == teacher:
                # Subject.objects.get(school_id=request.user.school_id, teacher=teacher)
                context['errors'] = 'This teacher is already assigned to this subject'
                return render(request, 'school/subject.html', context)
            # except Subject.DoesNotExist:
            #     pass
            subject.teacher = teacher
            subject.save()
            # SubjectTeacher.objects.create(
            #     subject=subject,
            #     teacher=teacher,
            #     created_by=request.user,
            #     school_id=request.user.school_id
            # )

            return redirect('school:management-subject', id)

        elif form == 'remteach':
            teach_id = request.POST.get('teacher')
            # teach = Staff.objects.get(school_id=request.user.school_id, id=teach_id)
            #
            # teach.delete()

            subject.teacher = None

            subject.save()

            return redirect('school:management-subject', id)

    return render(request, 'school/subject.html', context)


@login_required()
def academics(request):
    academic_sessions = AcademicYear.objects.filter(school_id=request.user.school_id)

    context = {
        'object_list': academic_sessions,
        'errors': ''
    }

    try:
        current_id = request.GET['cur']
        current = AcademicYear.objects.get(id=current_id)
        current.is_current = True
        current.save()
        return redirect('school:academics')
    except:pass

    if request.method == 'POST':
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')

        try:
            AcademicYear.objects.get(start_date__lte=start_date, end_date__gte=end_date)
            context['errors'] = 'Invalid academic session'
            return render(request, 'school/academics.html', context)
        except AcademicYear.DoesNotExist:
            pass

        ay = AcademicYear(
            start_date=start_date,
            end_date=end_date,
            school_id=request.user.school_id,
            created_by=request.user
        )

        ay.save()

        return redirect('school:academics')

    return render(request, 'school/academics.html', context)


@login_required()
def academic_details(request, id):
    academic = AcademicYear.objects.get(school_id=request.user.school_id, id=id)

    terms = AcademicTerm.objects.filter(school_id=request.user.school_id, academic_year=academic)

    context = {
        'object': academic,
        'terms': terms,
        'errors': ''
    }

    try:
        current_id = request.GET['cur']
        current = AcademicTerm.objects.get(id=current_id)
        current.is_current = True
        current.save()
        return redirect('school:academic-details', id)
    except:pass

    if request.method == 'POST':
        desc = request.POST.get('description')
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')

        try:
            AcademicTerm.objects.get(academic_year=academic, start_date__lte=start_date, end_date__gte=end_date, school_id=request.user.school_id)
            context['errors'] = 'Invalid date range'
            return render(request, 'school/academic_details.html', context)
        except AcademicTerm.DoesNotExist:
            pass
        sd = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        ed = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        monday1 = (sd - timedelta(days=sd.weekday()))
        monday2 = (ed - timedelta(days=ed.weekday()))

        # print('Weeks: ', (monday2 - monday1).days / 7)
        now = int((monday2 - monday1).days / 7)
        # print(now)

        at = AcademicTerm(
            description=desc,
            start_date=start_date,
            end_date=end_date,
            school_id=request.user.school_id,
            created_by=request.user,
            number_of_weeks=now,
            academic_year=academic
        )

        at.save()

        return redirect('school:academic-details', id)

    return render(request, 'school/academic_details.html', context)


@login_required()
def term_details(request, id):
    term = AcademicTerm.objects.get(school_id=request.user.school_id, id=id)

    attendances = Attendance.objects.filter(school_id=request.user.school_id, academic_term=term)

    result = None
    try:
        result = Result.objects.get(academic_term=term, school_id=request.user.school_id)
    except Result.DoesNotExist:pass

    classes = Class.objects.filter(school_id=request.user.school_id)

    schedules = ClassSchedule.objects.filter(academic_term=term, school_id=request.user.school_id)

    context = {
        'object': term,
        'result': result,
        'classes': classes,
        'attendances': attendances,
        'schedules': schedules
    }

    try:
        open_result = request.GET.get('result')

        if open_result == 'OPEN':
            res = Result(
                academic_year=term.academic_year,
                academic_term=term,
                status=0,
                created_by=request.user,
                school_id=request.user.school_id
            )

            res.save()

            return redirect('school:academic-term', id)
    except:pass

    if request.method == 'POST':
        classe = request.POST.get('class')

        try:
            classe = Class.objects.get(id=classe)
            return redirect('schedule:class', classe.id, id)
        except:pass

    return render(request, 'school/term.html', context)


@login_required()
def class_attendances(request, attendance_id):
    attendance = Attendance.objects.get(id=attendance_id, school_id=request.user.school_id)

    pupils = Pupil.objects.filter(classs=attendance.classs, school_id=request.user.school_id)

    context = {
        'object': attendance,
        'pupils': pupils
    }

    return render(request, 'school/class_attendances.html', context)

@login_required()
def class_results(request, id):
    classe = Class.objects.get(id=id)

    results = PupilResult.objects.filter(classe=classe, school_id=request.user.school_id, status=1)

    context = {
        'object': classe,
        'results': results
    }

    return render(request, 'school/class_results.html', context)


@login_required()
def pupils(request):

    context = {
        'object_list': Pupil.objects.filter(school_id=request.user.school_id)
    }

    return render(request, 'school/pupils.html', context)


@login_required()
def new_pupil(request):

    context = {
        'form': forms.PupilForm(initial={}, school_id=request.user.school_id)
    }

    if request.method == 'POST':
        profile = request.FILES.get('profile')

        form = forms.PupilForm(request.POST, school_id=request.user.school_id)

        if form.is_valid():
            classe = form.instance.classs

            form.instance.school_id = request.user.school_id

            form.instance.created_by = request.user

            form.instance.profile = profile

            pc = PupilClass(
                pupil=form.instance,
                classe=classe,
                created_by=request.user,
                school_id=request.user.school_id
            )

            form.save()
            pc.save()

            return redirect('school:pupils')


    return render(request, 'school/new_pupil.html', context)