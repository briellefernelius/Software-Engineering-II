from django.contrib import messages
from django.db.models import Sum
from course.models import Course, CourseUser
from users.models import CustomUser
from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from .models import Account
import stripe
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from mysite.views import Get_Messages

# Create your views here.

stripe.api_key = "sk_test_51KUIyfJVOaFYMiYoXv92CzSa1vIinDxC9OcaZBQY61oQOkxC3ZAuBMSKD58v" \
                 "bsOAMy6ANXI5zVMyL2OSasKjoo8X00SDET2xJG"


@login_required
def account(request):
    # courseuser = CourseUser.objects.all().filter(user_id=request.user.pk)
    # Use cookies to get user's courses
    item_list = request.session.get('courseuser')

    courseuser = list()
    print(f'courseuser: {item_list}')
    for course_id in item_list:
        courseuser.append(CourseUser.objects.get(id=course_id))

    # tuition = 0
    # for course in courseuser:
    #     tuition += course.course_id.credit_hours * 100

    form = AccountForm(request.POST or None)
    user = CustomUser.objects.get(pk=request.user.pk)

    if form.is_valid():
        user_account = Account.objects.all().filter(user=request.user.pk)
        account_user = Account.objects.all().filter(user=request.user.pk).count()

        account = Account()
        account.cardholder_name = request.POST.get('cardholder_name')
        account.card_number = request.POST.get('card_number')
        account.amount = request.POST.get('amount')
        account.cvc_number = request.POST.get('cvc_number')
        account.expiration_month = request.POST.get('expiration_month')
        account.expiration_year = request.POST.get('expiration_year')
        account.user = CustomUser.objects.get(pk=request.user.pk)

        card_num = account.card_number
        cvc = account.cvc_number
        exp_month = account.expiration_month
        exp_year = account.expiration_year
        amount = request.POST.get("amount")
        amount = int(amount) * 100
        card_num = str(card_num)
        cvc = str(cvc)
        sub_amount = request.POST.get("amount")
        sub_amount = int(sub_amount)

        if user.tuition - sub_amount < 0:
            print(f"!!amount cant be greater than tuition!!")
            messages.success(request, f'amount cant be greater than tuition!')
            return redirect('payment:amount_fail')

        print(f"cvc {cvc}")
        print(f"exp_year {exp_year}")
        print(f"exp_month {exp_month}")
        print(f"card_num {card_num}")

        token = stripe.Token.create(
            card={
                "number": card_num,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc
            },
        )

        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token,  # obtained above
            description="Tuition Charge"
        )

        # if cvc is not '314' and card_num is not '4242424242424242' and exp_month is not 3 and exp_year is not 2023:
        #     return redirect('payment:card_decline')

        user.tuition = user.tuition - sub_amount
        print(f"Tuition: {user.tuition}")
        account.save()
        user.save()

        #return redirect('payment:payment_success')

    # tuition should probably be saved to the user's account, after it fully works
    context = {'form': form, 'total_tuition': user.tuition}
    notification = Get_Messages(request)
    context.update(notification)  # merging the context dictionary with the messages dictionary
    return render(request, 'payment/account.html', context)


@login_required
def amount_fail(request):
    return render(request, 'payment/fail_page.html')


@login_required
def payment_success(request):
    return render(request, 'payment/success_page.html')


@login_required
def card_decline(request):
    return render(request, 'payment/card_declined.html')
