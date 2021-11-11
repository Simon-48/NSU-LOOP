from django.shortcuts import render

# Create your views here.
from payment.models import Payment
from django.shortcuts import render

# view function for make payment page
def make_payment(request):
    return render(request, 'payments/make_payment.html')

# view function for confirming payment
def confirm_payment(request):
    # getting form value
    phone = request.GET.get("phone")
    transaction_id = request.GET.get("transaction_id")

    context = {'confirm': False}

    # confirm payment
    payment = Payment.objects.filter(mobile_number=phone, transaction_id=transaction_id, verified=False)
    if len(payment) > 0:
        payment = payment[0]
        payment.verified = True
        payment.save()
        context['confirm'] = True

    return render(request, 'payments/confirm_payment.html', context)