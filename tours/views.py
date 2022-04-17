from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render
from django.views import View
from tours.data import data
import random


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')


class TourView(View):
    def get(self, request, id, *args, **kwargs):
        if id is None or id < 1 or id > 16:
            raise Http404

        tours_id = data.tours.get(id)
        stars = "★" * int(data.tours.get(id).get("stars"))
        tours_departures = data.tours.get(id).get("departure")
        price = data.tours.get(id).get("price")
        price = '{:,}'.format(price).replace(',', ' ')

        context = {"tours_id": tours_id,
                   "stars": stars,
                   "departures_tours": data.departures[tours_departures],
                   "price": price,
                   "title": data.title,
                   "departures": data.departures}

        return render(request, "tour.html", context)


class MainView(View):
    def get(self, request, *args, **kwargs):
        numbers_tours = [i+1 for i in range(len(data.tours))]
        random_numbers_tours = random.sample(numbers_tours, 6)
        random_tours = dict()

        for num in random_numbers_tours:
            random_tours[num] = data.tours[num]

        context = {"subtitle": data.subtitle,
                   "description": data.description,
                   "tours_id": random_tours,
                   "title": data.title,
                   "departures": data.departures}

        return render(request, "index.html", context)


class DepartureView(View):
    def get(self, request, departure, *args, **kwargs):
        hotels = dict()
        lst_price = []
        lst_nights = []

        for values in data.tours.values():
            if values["departure"] == departure:
                lst_price.append(values["price"])
                lst_nights.append(values["nights"])

        price_min = '{:,}'.format(min(lst_price)).replace(',', ' ')
        price_max = '{:,}'.format(max(lst_price)).replace(',', ' ')
        nights_min = min(lst_nights)
        nights_max = max(lst_nights)

        for key, values in data.tours.items():
            if departure == values.get("departure"):
                hotels[key] = values

        depart_count = len(hotels)

        context = {"depart_count": depart_count,
                   "hotels": hotels,
                   "depart_city": data.departures[departure],
                   "price_min": price_min,
                   "price_max": price_max,
                   "nights_min": nights_min,
                   "nights_max": nights_max,
                   "title": data.title,
                   "departures": data.departures}

        return render(request, "departure.html", context)
