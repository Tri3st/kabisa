from random import randint
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Quote
from .serializers import QuoteSerializer


# Create your views here.
def get_quotes():
    quotes = []
    with open('./assignment/static/json/quotes.json') as f:
        for line in f:
            qline = line.split(",")
            quotes.append({
                'author': qline[0],
                'quote': qline[1]
            })
    return quotes

def index(request):
    """show a rondom quote"""
    nr_of_quotes = Quote.objects.all().count()
    random_index = randint(0, nr_of_quotes)
    quote = Quote.objects.get(pk=random_index)
    return render(request, 'random_quote.html', {'quote': quote})

@csrf_exempt
def quote_list(request):
    if request.method == 'GET':
        quotes = Quote.objects.all()
        serializer = QuoteSerializer(quotes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = QuoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def quote_detail(request, pk):
    """Retrieve, update or delete a quote"""
    try:
        quote = Quote.objects.get(pk=pk)
    except Quote.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = QuoteSerializer(quote)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = QuoteSerializer(quote, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        quote.delete()
        return HttpResponse(status=204)

@csrf_exempt
def quote_detail_xml(request, pk):
    pass


@csrf_exempt
def quote_detail_like(request, pk):
    """like a quote"""
    try:
        quote = Quote.objects.get(pk=pk)
    except Quote.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        quote.likes += 1
        quote.save()
        return HttpResponse(status=200)

    return HttpResponse(status=400)

# def random_quote(request):
#     quotes = Quote.objects.all()
#     random_index = randint(0, len(quotes))
#     quote = quotes[random_index]
#     return render(request, 'random_quote.html', {'quote': quote})
def random_quote(request):
    """show a rondom quote"""
    nr_of_quotes = Quote.objects.count()
    random_index = randint(0, nr_of_quotes)

    try:
        quote = Quote.objects.get(pk=random_index)
    except Quote.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = QuoteSerializer(quote)
        return JsonResponse(serializer.data)

