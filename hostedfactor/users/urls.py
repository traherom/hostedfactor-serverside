from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from users import views

urlpatterns = [
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, name='logout'),

    url(r'^profile/edit/',
        views.UserProfileEdit.as_view(),
        name='profile-edit'),
    url(r'^profile/password/$',
        auth_views.password_change,
        { 'template_name': 'users/password_change_form.html' },
        name='profile-pw'),
    url(r'^profile/password/done/$',
        auth_views.password_change_done,
        { 'template_name': 'users/password_change_done.html' },
        name='password_change_done'),

    url(r'^profile/password/reset/$',
        auth_views.password_reset,
        { 'template_name': 'users/password_reset_form.html' },
        name='password_reset'),
    url(r'^profile/password/reset/done/$',
        auth_views.password_reset_done,
        { 'template_name': 'users/password_reset_emailed.html' },
        name='password_reset_done'),
    url(r'^profile/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        { 'template_name': 'users/password_reset_confirm.html' },
        name='password_reset_confirm'),
    url(r'^profile/password/reset/complete/$',
        auth_views.password_reset_complete,
        { 'template_name': 'users/password_reset_complete.html' },
        name='password_reset_complete'),
]
