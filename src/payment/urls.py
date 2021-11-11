from django.urls import path
from .views import confirm_payment, make_payment 

app_name = 'payment'

urlpatterns = [
    path('make/', make_payment, name="make-payment"),
    path('confirm/', confirm_payment, name="confirm-payment"),
]
