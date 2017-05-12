from django.conf.urls import url
from . import views

app_name = 'debtinfo'

urlpatterns = [
    url(r'^info/search', views.SearchDebtor.as_view(), name='search_debtor'),
    url(r'^info/view', views.ViewDebtors.as_view(), name='view_debtors'),
    url(r'^info/download', views.download_table, name='download_table')
]
