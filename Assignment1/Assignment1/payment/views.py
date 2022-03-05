from django.db.models import Sum
from course.models import Course, CourseUser
from users.models import CustomUser
from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from .models import Account
import stripe
from django.views.generic import View
# Create your views here.

stripe.api_key = "sk_test_51KUIyfJVOaFYMiYoXv92CzSa1vIinDxC9OcaZBQY61oQOkxC3ZAuBMSKD58vbsOAMy6ANXI5zVMyL2OSasKjoo8X00SDET2xJG"


def account(request):
    courseuser = CourseUser.objects.all().filter(user_id=request.user.pk)
    tuition = 0
    form = AccountForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            card_num = request.POST.get('card_number')
            exp_month = request.POST.get('expiration_month')
            exp_year = request.POST.get('expiration_year')
            exp_month = int(exp_month)
            exp_year = int(exp_year)
            cvc = request.POST.get('cvc_number')
            amount = request.POST.get("amount")
            amount = int(amount) * 100
            sub_amount = request.POST.get("amount")
            sub_amount = int(sub_amount)

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
            tuition = tuition - sub_amount
            form.save()
    for course in courseuser:
        tuition += course.course_id.credit_hours * 100

    return render(request, 'payment/account.html', {'form': form, 'tuition': tuition})
