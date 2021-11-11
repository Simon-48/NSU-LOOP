from django.urls import path
from .views import confirm_jackpot, make_jackpot 

app_name = 'jackpot'

urlpatterns = [
    path('make/', make_jackpot, name="make-jackpot"),
    path('confirm/', confirm_jackpot, name="confirm-jackpot"),
]
