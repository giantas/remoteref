from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'debtinfo'

urlpatterns = [
    url(r'^info/search', login_required(views.SearchDebtorListView.as_view()),
        name='search_debtor'),
    url(r'^info/view', login_required(views.ViewDebtorsListView.as_view()),
        name='view_debtors'),
    url(r'^info/download', login_required(views.download_table), name='download_table')
]
