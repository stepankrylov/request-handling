from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv

from statsmodels.compat import urlencode

from app.settings import BUS_STATION_CSV

data = []
def index(request):
    with open(BUS_STATION_CSV) as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            data.append({'Name': line["Name"], 'Street': line["Street"], 'District': line["District"]})
    return redirect(reverse(bus_stations))


def bus_stations(request):

    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(data, 10)

    page = paginator.page(page_num)
    new_data = page.object_list

    if page.has_next() == True:
        next_page_url = reverse(bus_stations) + '?%s' % urlencode({'page': page_num + 1})
    else:
        next_page_url = None

    if page.has_previous() == True:
        prev_page_url = reverse(bus_stations) + '?%s' % urlencode({'page': page_num - 1})
    else:
        prev_page_url = None

    return render_to_response('index.html', context={
        'bus_stations': new_data,
        'current_page': page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

