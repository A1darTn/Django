from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import csv
from pagination.settings import BUS_STATION_CSV

def index(request):
    return redirect(reverse("bus_stations"))



BUS_STATIONS = []
with open(BUS_STATION_CSV, mode='r',encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        BUS_STATIONS.append(row)


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    

    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(BUS_STATION_CSV, 10)
    page = paginator.get_page(page_number)

    context = {
        "bus_stations": BUS_STATIONS,
        "page": page,
    }
    return render(request, "stations/index.html", context)
