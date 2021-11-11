from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    """
    This method will create a home page request. It will pass logged in user name and a welcome message 
    in the home page.
       
    :param name: request - used to generate responses(Http) depending on the request that it receives
    :param type: HttpResponse
    :return: returns home page
    """
    user = request.user
    welcome = 'WELCOME TO THE NSULOOP SOCIAL MEDIA PLATFORM'

    context = {
        'user': user,
        'welcome' : welcome,
    }
    return render(request, 'main/home.html', context)