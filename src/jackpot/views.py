from jackpot.models import Jackpot
from django.shortcuts import render

# view function for make jackpot page
def make_jackpot(request):
    """
    This method will return the url of make_jackpot html page.
       
    :param name: request - used to generate responses(Http) depending on the request that it receives
    :param type: HttpResponse
    :return: returns posts page
    
    """ 
    return render(request, 'jackpots/make_jackpot.html')

# view function for confirming jackpot
def confirm_jackpot(request):
    """
    This method will get lucky pick id and verify the lucky pick id. If verification is successful
    then will return the url of confirm_jackpot html page. 
       
    :param name: request - used to generate responses(Http) depending on the request that it receives
    :param type: HttpResponse
    :return: returns posts page
    
    """

    # getting form value
    lucky_id = request.GET.get("lucky_id")

    context = {'confirm': False}

    # confirm jackpot
    jackpot = Jackpot.objects.filter(lucky_id=lucky_id, verified=False)
    if len(jackpot) > 0:
        jackpot = jackpot[0]
        jackpot.verified = True
        jackpot.save()
        context['confirm'] = True

    return render(request, 'jackpots/confirm_jackpot.html', context)