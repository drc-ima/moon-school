import decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from apps.pupil.models import Class
from apps.school.models import AcademicYear, AcademicTerm
from utils.randoms import payment_id
from .models import *
# Create your views here.


@login_required()
def fee_setup(request):
    items = FeeItem.objects.filter(school_id=request.user.school_id)
    session_list = AcademicYear.objects.filter(school_id=request.user.school_id)

    context = {
        'object_list': items,
        'sessions': session_list
    }

    if request.method == 'POST':
        form = request.POST.get('form')
        if form == 'new':
            description = request.POST.get('description')

            FeeItem.objects.create(
                item=description,
                school_id=request.user.school_id,
                created_by=request.user
            )

            return redirect('finance:setup')
        elif form == 'remove':
            item_id = request.POST.get('item')
            item = FeeItem.objects.get(id=item_id)

            item.delete()

            return redirect('finance:setup')

    return  render(request, 'finance/setup.html', context)


@login_required()
def sessions(request):

    session_list = AcademicYear.objects.filter(school_id=request.user.school_id)

    context = {
        'object_list': session_list
    }

    return render(request, 'finance/sessions.html', context)


@login_required()
def fee_schedules(request, term_id):
    term = AcademicTerm.objects.get(school_id=request.user.school_id, id=term_id)

    schedules = FeeSchedule.objects.filter(academic_term=term, school_id=request.user.school_id)

    student_statuses = [('D', 'Day'), ('FD', 'Fresh Day'), ('B', 'Boarder'), ('FB', 'Fresh Boarder')]

    classes = Class.objects.filter(school_id=request.user.school_id)

    context = {
        'object_list': schedules,
        'term': term,
        'student_statuses': student_statuses,
        'classes': classes
    }

    return render(request, 'finance/schedules.html', context)


@login_required()
def new_schedule(request, term_id):
    context = {
        'classes': Class.objects.filter(school_id=request.user.school_id),
        'fee_items': FeeItem.objects.filter(school_id=request.user.school_id),
        'errors': ''
    }

    term = AcademicTerm.objects.get(id=term_id, school_id=request.user.school_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        classe = request.POST.get('class')

        try:
            fs = FeeSchedule.objects.get(classe_id=classe, student_status=status, academic_term=term, school_id=request.user.school_id)
            context['errors'] = f"There's already a fee schedule for {fs.classe.description} " \
                                f"{fs.get_student_status_display()} students"
            return render(request, 'finance/new_schedule.html', context)
        except:pass

        nfs = FeeSchedule(
            academic_term=term,
            classe_id=classe,
            student_status=status,
            created_by=request.user,
            school_id=request.user.school_id
        )

        nfs.save()
        total = 0.00
        import re
        for data in request.POST:
            if re.search('[0-9]', data):
                data = data.split("-")
                field = request.POST.get(f"{data[0]}-{data[1]}")

                if field:
                    try:
                        fee_item = FeeItem.objects.get(id=data[0], school_id=request.user.school_id)
                        print(fee_item)
                        nfsi = FeeScheduleItem(
                            fee_schedule=nfs,
                            fee_item=fee_item,
                            amount=field,
                            created_by=request.user,
                            school_id=request.user.school_id
                        )
                        nfsi.save()
                        total += float(field)
                    except FeeItem.DoesNotExist:pass

        nfs.amount = total
        nfs.save()

        return redirect('finance:schedules', term_id)

    return render(request, 'finance/new_schedule.html', context)


@login_required()
def fee_payments(request):

    term = None

    try:
        term = AcademicTerm.objects.get(is_current=True, school_id=request.user.school_id)
    except:pass

    context = {
        'object_list': StudentPayment.objects.filter(school_id=request.user.school_id, student_fee__fee_schedule__academic_term__is_current=True),
        'term': term,
        'classes': Class.objects.filter(school_id=request.user.school_id)
    }
    try:
        term = request.GET.get('term')
        classe = request.GET.get('class')

        fee_payments = StudentPayment.objects.filter(Q(student_fee__pupil__first_name__icontains=term)
                                                     |Q(student_fee__pupil__last_name__icontains=term)
                                                     |Q(student_fee__pupil__classs_id=classe)
                                                     |Q(student_fee__fee_schedule__academic_term=AcademicTerm.objects.get(is_current=True, school_id=request.user.school_id))
                                                     &Q(school_id=request.user.school_id))

        context['object_list'] = fee_payments
        return render(request, 'finance/fee_payments.html', context)
    except:pass

    return render(request, 'finance/fee_payments.html', context)


@login_required()
def new_payment(request):
    term = AcademicTerm.objects.get(is_current=True, school_id=request.user.school_id)
    classes = Class.objects.filter(school_id=request.user.school_id)

    context = {
        'errors': '',
        'term': term,
        'classes': classes
    }

    if request.method == 'POST':
        import num2words
        class_id = request.POST.get('class')
        pupil_id = request.POST.get('pupil')
        amount = request.POST.get('amount')

        classe = Class.objects.get(id=class_id, school_id=request.user.school_id)
        pupil = None

        try:
            pupil = Pupil.objects.get(id=pupil_id, school_id=request.user.school_id)
        except Pupil.DoesNotExist:
            context['errors'] = 'No student selected'
            return render(request, 'finance/new_payment.html', context)

        fs = None

        try:
            fs = FeeSchedule.objects.get(classe=classe, student_status=pupil.status, school_id=request.user.school_id)
        except FeeSchedule.DoesNotExist:
            context['errors'] = f'There is no school fees scheduled for {classe.description} {pupil.get_status_display()} students'
            return render(request, 'finance/new_payment.html', context)

        try:
            sf = StudentFee.objects.get(fee_schedule=fs, pupil=pupil, school_id=request.user.school_id)

            sps = StudentPayment.objects.filter(student_fee=sf).count() + 1

            sps = '{0:03}'.format(sps)

            new_student_fee = StudentPayment(
                student_fee=sf,
                amount=amount,
                payment_id=payment_id(pupil.first_name, pupil.last_name, term.description, sps),
                created_by=request.user,
                school_id=request.user.school_id
            )
            new_student_fee.save()

            sf.amount_paid += decimal.Decimal(amount)

            if sf.amount_paid != sf.amount_to_pay:

                sf.remaining = fs.amount - sf.amount_paid

                sf.arrears = fs.amount - sf.amount_paid
            else:
                sf.fully_paid = True

            sf.save()

            if new_student_fee.amount == sf.amount_to_pay:
                srs = Receipt.objects.filter(student_payment=new_student_fee).count() + 1

                srs = '{0:03}'.format(srs)
                receipt = Receipt(
                    student_payment=new_student_fee,
                    status=1,
                    created_by=request.user,
                    words=num2words.num2words(new_student_fee.amount),
                    school_id=request.user.school_id,
                    receipt_id=payment_id(pupil.first_name, pupil.last_name, term.description, srs)
                )

                receipt.save()

                return redirect('finance:payment-receipt', receipt.receipt_id)
            else:
                srs = Receipt.objects.filter(student_payment=new_student_fee).count() + 1

                srs = '{0:03}'.format(srs)
                receipt = Receipt(
                    student_payment=new_student_fee,
                    status=0,
                    created_by=request.user,
                    words=num2words.num2words(new_student_fee.amount),
                    school_id=request.user.school_id,
                    receipt_id=payment_id(pupil.first_name, pupil.last_name, term.description, srs)
                )

                receipt.save()
                return redirect('finance:payment-receipt', receipt.receipt_id)

        except StudentFee.DoesNotExist:
            nfs = FeeSchedule.objects.get(classe=classe, student_status=pupil.status)

            if decimal.Decimal(amount) == nfs.amount:

                nsf = StudentFee(
                    fee_schedule=nfs,
                    pupil=pupil,
                    amount_to_pay=nfs.amount,
                    amount_paid=amount,
                    created_by=request.user,
                    fully_paid=True,
                    school_id=request.user.school_id
                )

                nsf.save()

                sps = StudentPayment.objects.filter(student_fee=nsf).count() + 1

                sps = '{0:03}'.format(sps)

                new_student_fee = StudentPayment(
                    student_fee=nsf,
                    amount=amount,
                    payment_id=payment_id(pupil.first_name, pupil.last_name, term.description, sps),
                    created_by=request.user,
                    school_id=request.user.school_id
                )
                new_student_fee.save()

                if pupil.status == 'FD':
                    pupil.status = 'D'
                elif pupil.status == 'FB':
                    pupil.status = 'B'

                pupil.save()

                srs = Receipt.objects.filter(student_payment=new_student_fee).count() + 1

                srs = '{0:03}'.format(srs)

                receipt = Receipt(
                    student_payment=new_student_fee,
                    status=1,
                    created_by=request.user,
                    words=num2words.num2words(new_student_fee.amount),
                    school_id=request.user.school_id,
                    receipt_id=payment_id(pupil.first_name, pupil.last_name, term.description, srs)
                )

                receipt.save()

                return redirect('finance:payment-receipt', receipt.receipt_id)
            else:
                context['errors'] = f'Fresh amount fees to be paid is GHS {nfs.amount}'
                return render(request, 'finance/new_payment.html', context)

    return render(request, 'finance/new_payment.html', context)


@login_required()
def class_pupils(request, class_id):

    classe = Class.objects.get(school_id=request.user.school_id, id=class_id)

    pupils = list(Pupil.objects.filter(classs=classe,school_id=request.user.school_id).values('id', 'first_name', 'last_name'))

    return JsonResponse(pupils, safe=False)

@login_required()
def receipt_view(request, receipt_id):

    receipt = Receipt.objects.get(receipt_id=receipt_id)

    context = {
        'object': receipt
    }

    return render(request, 'finance/receipt.html', context)