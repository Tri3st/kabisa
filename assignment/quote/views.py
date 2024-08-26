import re
from random import randint
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Quote
from .serializers import QuoteSerializer
from openai import OpenAI


# Create your views here.
def get_quotes():
    """get quotes from json file"""
    # TODO get more quotes online and merge these into tge database
    quotes = []
    with open('./assignment/static/json/quotes.json') as f:
        for line in f:
            qline = line.split(",")
            quotes.append({
                'author': qline[0],
                'quote': qline[1]
            })
    return quotes

def get_some_more_quotes(number=10):
    """
    get some files from openai
    first we get some quotes from OpenAI, then we format the quotes to fit our database
    then we check if the quote exists (TODO this check must be implemented better)
    if the quote does not exist, we add it to the database
    """
    client = OpenAI(
        organization="org-6X4qNlDdQVxVHwXHw4EMs6qd",
        project="proj_nGvsxdEL8zsn17hQyEmYse6O"
    )
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":f"Generate {number} quotes from famous people"}],
        stream=True,
    )

    for chunk in stream:
        print(chunk)
        if chunk.choices[0].delta.content is not None:

            raw_quotes_text = chunk.choices[0].delta.content
            quotes = raw_quotes_text.split("\n\n")
            # a quote is given as "1. **<author>**: <quote>"
            # the first line is the introduction and the last one is a sumary
            quotes_to_add = []
            for quote in quotes[1:-1]:
                # get author and quote
                q2 = quote.split(":")
                regex = re.findall(r"^\d+\. \*\*([a-zA-Z .]+)\*\*$", q2[0])
                author = regex[0]
                regex2 = re.findall(r"^\s*“([a-zA-Z ,.:!’?]+)”$", q2[1])
                readable_quote = regex2[0].replace("’", "\'").strip()
                qq = {
                    'author': author,
                    'quote': str(readable_quote)
                }
                print(qq)
                quotes_to_add.append(qq)
            # check if quote already exists in database
            # if not, add it to the database
            for q in quotes_to_add:
                if not Quote.objects.filter(quote=q['quote']).exists():
                    Quote.objects.create(author=q['author'], quote=q['quote'])
                    print(f"Added quote: {q['quote']}")


def index(request):
    """show a rondom quote"""
    nr_of_quotes = Quote.objects.all().count()
    random_index = randint(0, nr_of_quotes)
    quote = Quote.objects.get(pk=random_index)
    return render(request, 'random_quote.html', {'quote': quote})


@csrf_exempt
def quote_list(request):
    """List all quotes or create a new quote"""
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
    """retrieve a quote in xml format"""
    pass


@csrf_exempt
def quote_detail_like(request, pk):
    """like a quote"""
    # TODO not finished!
    try:
        quote = Quote.objects.get(pk=pk)
    except Quote.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = QuoteSerializer(quote, data=data)
        quote.likes += 1
        quote.save()
        return JsonResponse(serializer.data, status=200)

    return JsonResponse(status=400)


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


def show_quotes_in_order_of_likes(request):
    """show quotes in order of likes"""
    # we want to get the top 3 of the django database entries based on the number of likes
    quotes = Quote.objects.order_by('-likes')[:3]

