from .forms import SearchForm
from .models import Profile, Debtor
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.template.defaultfilters import pluralize
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.utils.decorators import method_decorator
import re
import openpyxl


class SearchDebtor(ListView, FormMixin):
    model = Profile
    template_name = 'debtinfo/search_debtor.html'
    context_object_name = 'debtors'
    form_class = SearchForm

    def get_queryset(self):
        if 'q' in self.request.GET and self.request.GET['q'].strip():
            search_query = self.request.GET['q'].strip()
            field_list = ['id_number', 'cell']
            obj = search_fields(search_query, field_list, model=self.model)
            if obj.count() == 0:
                messages.error(
                    self.request, 'Customer with ID or Contact number "%s" NOT found.' % search_query)
            else:
                result_count = obj.count()
                messages.info(self.request, "{0} {1} found for search '{2}'".format(
                    result_count, counter(result_count, 'result', 'results'), search_query))

        else:
            obj = self.model.objects.none()
            messages.info(
                self.request, 'Search for a Customer by national ID or Contact numbers.')

        return obj

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            obj = self.form.save(commit=False)
            self.object = obj.save()

            messages.success(request, 'Query successful! ')
            return HttpResponseRedirect(reverse_lazy('debtinfo:search_debtors'))

        return self.get(request, *args, **kwargs)

    def get_success_url(self):
        return HttpResponseRedirect(reverse_lazy('debtinfo:search_debtors'))


class ViewDebtors(ListView):
    model = Debtor
    context_object_name = 'debtors'
    template_name = 'debtinfo/view_debtors.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ViewDebtors, self).dispatch(request, *args, **kwargs)


def download_table(request):
    debtors = Debtor.objects.all()

    wb = openpyxl.Workbook(write_only=True)
    debtors_sheet = 'Debtors'
    wb.create_sheet(debtors_sheet)
    sheet = wb.get_sheet_by_name(debtors_sheet)
    sheet.append(['First Name', 'Last Name', 'ID', 'Contact'])
    for details in debtors:
        sheet.append([details.debtor.first_name,
                      details.debtor.last_name, details.id_number, details.cell])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=debtors.xlsx'

    wb.save(response)
    wb.close()
    return response


def counter(count, singular, plural):
    """Return the appropriate plural term with regard to the count."""

    return pluralize(count, singular + ',' + plural)


# Search snippet
def search_fields(query_string, field_list, model):
    entry_query = get_query(query_string, field_list)
    found_entries = model.objects.filter(entry_query)

    return found_entries


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__iexact" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
