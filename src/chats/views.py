from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from chats.forms import ChatModelForm
from chats.models import Chat


@login_required
def message_create_list_view(request, to_user_id):
    """
    This method will create a post request on one form. it will add a chat entry for successful post.
    This method will also show the list of chats with the specific person
    This method will only load this page if the user is logged in.

    :param request - used to generate responses(Http) depending on the request that it receives
    :param to_user_id - this variable contains the receiver user id (to whom the user is interested
     to send message).
    :param : HttpResponse
    :return: returns chat page
    """

    chat_form = ChatModelForm()
    from_user = request.user
    to_user = User.objects.get(id=to_user_id)

    chats = Chat.objects.filter(
        from_user_id__in=[
            from_user.id,
            to_user_id
        ],
        to_user_id__in=[
            from_user.id,
            to_user_id
        ]
    )

    if 'submit_chat_form' in request.POST:
        data = {
            'from_user_id': from_user.id,
            'to_user_id': to_user_id,
            'message': request.POST.get('message'),
        }
        if not data.get("message"):
            raise ValueError()
        chat_object = Chat.objects.create(
            **data
        )

    context = {
        'chats': chats,
        'chat_form': chat_form,
        'to_user': to_user
    }

    return render(request, 'chats/main.html', context)


@login_required
def user_list_view(request):
    """
    This method will show all available users. Clicking any user will redirect to the chat inbox page.
    :param request: used to generate responses(Http) depending on the request that it receives
    :return: returns chat page
    """

    users = User.objects.all().exclude(id=request.user.id).values("id", "username")

    context = {
        'users': users,
    }
    return render(request, 'chats/user_list.html', context)
