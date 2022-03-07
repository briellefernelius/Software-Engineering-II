from django.db.models import Sum
from course.models import Course, CourseUser
from users.models import CustomUser
from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from .models import Account
import stripe
from django.views.generic import View
from mysite.views import Get_Messages
# Create your views here.

stripe.api_key = "sk_test_51KUIyfJVOaFYMiYoXv92CzSa1vIinDxC9OcaZBQY61oQOkxC3ZAuBMSKD58vbsOAMy6ANXI5zVMyL2OSasKjoo8X00SDET2xJG"


def account(request):
    #courseuser = CourseUser.objects.all().filter(user_id=request.user.pk)
    # Use cookies to get user's courses
    item_list = request.session.get('courseuser')
    courseuser = list()
    print(f'courseuser: {item_list}')
    for course_id in item_list:
        courseuser.append(CourseUser.objects.get(id=course_id))

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
        # tuition should probably be saved to the user's account, after it fully works
    context = {'form': form, 'tuition': tuition}
    messages = Get_Messages(request)
    context.update(messages)  # merging the context dictionary with the messages dictionary
    return render(request, 'payment/account.html', context)
