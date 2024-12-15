from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
# from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", login_view,name='login'),
    path('custom-admin/dashboard/', admin_dashboard, name='custom_admin_dashboard'),
    path("register/", register_view,name='register')
    ,
    path("home/", home_view,name='home'),
    path('profile/', profile_view, name='profile'),
    path('chat/', chat_view, name='chat'),

    path('new_event/', new_event_view, name='new_event'),
    # path('update_event/<int:event_id>/', update_event_view, name='update_event'),
    path('edit-event/<int:event_id>/', edit_event, name='edit_event'),
    
    path('delete-event/<int:event_id>/', delete_event_view, name='delete_event'),
    path('search/', search_events, name='search_events'),
    path('filter/', filter_events, name='filter_events'),
    
    path('logout/', logout_view, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)