from django.urls import path

from chats.views import message_create_list_view, user_list_view

app_name = 'chats'

urlpatterns = [
    path('', user_list_view, name='user_list'),
    path('<int:to_user_id>/', message_create_list_view, name='chat-view'),

]