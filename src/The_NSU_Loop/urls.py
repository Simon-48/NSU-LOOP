from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home-view'),
    path('accounts/', include('allauth.urls')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('payments/', include('payment.urls', namespace='payments')),
    path('jackpots/', include('jackpot.urls', namespace='jackpots')),
    path('chats/', include('chats.urls', namespace='chats')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)