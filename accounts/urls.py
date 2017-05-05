from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'register/$', views.register_user, name='register_user'),
    url(r'login/$', views.login_user, name='login_user'),
    url(r'logout/$', views.logout_user, name='logout_user'),
    url(r'user/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_user,
        name='activate_user'
        )
]
