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
    item_list = list()
    tuition = 0
    form = AccountForm(request.POST or None)
    if form.is_valid():
        #form.save()
        card_num = request.POST.get('card_number')
        # exp_month = request.POST.get['expiration_date']
        # exp_year = request.POST.get['expiration_date']
        cvc = request.POST.get('cvc_number')
        amount = request.POST.get("amount")
        amount = int(amount) * 100
        token = stripe.Token.create(
            card={
                "number": card_num,
                "exp_month": 3,
                "exp_year": 2023,
                "cvc": cvc
            },
        )

        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token,  # obtained above
            # source="tok_visa", # obtained with Stripe.js (JS)
            description="Tuition Charge"
        )
    for course in courseuser:
        tuition += course.course_id.credit_hours * 100
    print(f"CustomUser.courses = {item_list}")
    return render(request, 'payment/account.html', {'item_list': item_list, 'form': form, 'tuition': tuition})





