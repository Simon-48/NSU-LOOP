from django.urls import path
from .views import ( 
    invites_received_view, 
    my_profile_view,
    profiles_list_view, 
    ProfileDetailView,
    ProfileListView,
    send_invatation,
    remove_from_friends,
    accept_invatation,
    reject_invatation,
    friend_profile_view,
    find_view,
    save_talen_poll,
    search_friends,
    search_post,
    talent_poll,
)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('send-invite/', send_invatation, name='send-invite'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('my-invites/acctept/', accept_invatation, name='accept-invite'),
    path('my-invites/reject/', reject_invatation, name='reject-invite'),
    path('profile/<int:userId>', friend_profile_view, name='friend-profile-view'),
    path("find/", find_view, name="find-view"),
    path("find/posts", search_post, name="search-post"),
    path("find/friends", search_friends, name='search-friends'),
    path("tpoll", talent_poll, name="talent-poll"),
    path("tpoll/<str:skill>/<int:userId>", save_talen_poll, name="talent-poll-vote")
]