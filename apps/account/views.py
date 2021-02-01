from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify

from apps.account.models import User
from apps.school.models import School
from utils.randoms import institution_id, account_id



@login_required()
def dashboard(request):
    return render(request, 'account/dashboard.html')


def user_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    context = {
        'errors': ''
    }

    if request.method == 'POST':
        try:
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('account:dashboard')
            elif user is not None and not user.is_active:
                errors = 'This account is inactive'
                context['errors'] = errors
                return render(request, 'account/login.html', context)
            else:
                errors = 'Please enter a correct email address and password. Note that both fields are case-sensitive'
                context['errors'] = errors
                return render(request, 'account/login.html', context)
        except:
            errors = 'Email does not exist'
            context['errors'] = errors
            return render(request, 'account/login.html', context)
    return render(request, 'account/login.html', context)


@login_required()
def user_logout(request):
    logout(request)
    return redirect('login')


def signup_user(request):
    email = request.POST.get('email')
    # first_name = request.POST.get('first_name', None)
    # middle_name = request.POST.get('middle_name', None)
    # last_name = request.POST.get('last_name', None)
    # password = request.POST.get('password', None)

    ss1 = None

    try:
        ss1 = request.session['ss1']
    except:
        pass

    context = {
        'errors': '',
        'ss1': ss1
    }

    if request.method == 'POST':
        try:
            User.objects.get(username=email)
            context['errors'] = "This email has already been registered"
            return render(request, 'account/signup1.html', context)
        except User.DoesNotExist:
            pass

        request.session['ss1'] = request.POST

        return redirect(reverse_lazy('account:register-school'))

    return render(request, 'account/signup1.html', context)


def signup_school(request):
    name = request.POST.get('institution', None)
    logo = request.FILES.get('logo', None)
    phone_number = request.POST.get('phone_number', None)
    domain = request.POST.get('domain', None)
    gps = request.POST.get('gps', None)

    # ss1 = None

    try:
        ss1 = request.session['ss1']
    except:
        return redirect(reverse_lazy('account:register-user'))

    context = {
        'errors': '',
        'ss1': ss1
    }

    if request.method == 'POST':

        try:
            School.objects.get(domain=domain)
            context['errors'] = "There's already a school with this domain registered"
            return render(request, 'account/signup2.html', context)
        except School.DoesNotExist:
            pass

        inst_count = School.objects.count() + 1

        inst_count = '{0:04}'.format(inst_count)

        user_count = User.objects.filter(school_id=institution_id(name, inst_count)).count() + 1

        user_count = '{0:04}'.format(user_count)

        user = User(
            username=ss1['email'],
            email=ss1['email'],
            first_name=ss1['first_name'],
            middle_name=ss1['middle_name'],
            last_name=ss1['last_name'],
            slug="-".join((slugify(ss1['first_name']), slugify(ss1['last_name']))),
            user_type='SAD',
            account_id=account_id(name, ss1['first_name'], ss1['last_name'], user_count),
            school_id=institution_id(name, inst_count),
        )

        user.set_password(ss1['password'])

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

        request.session['ss1'] = {}

        return redirect('login')

    return render(request, 'account/signup2.html', context)

