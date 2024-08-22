# Kabisa Assignment

= Author: Martin van Diest
= Date: 22-08-2024
= Estimated time spent on assignment: 5 hours


## The assignment

The assignment was to create a web service. To generate random quotes from famouse people.

I want to collect Quotes and allow users to login and remember the quotes they liked.

So I need a database to collect quotes, authors, likes and also users

I need and API to view the quotes and an endpoint to show a random quote.

## Result

I was not able to get the whole thing running on a webserver. So I made a docker container for the database.
This holds user information and authentication.
Also it holds the quotes, authors and number of likes.

The frondend/backend is made with django/djangoRestFramework

I tried to let it look a as nice as possible. But my design-skills are not that the best.

## Conclusion

It was fun to do and try to see how far I can get with the assignment.
Looking forward to our talk.

## Instructions

- fork the repository

- run the docker in the ./docker directory 
```[bash]
$ docker compose -f docker-compose.yml up --build
```

- cd ./assignment

- first time django :

```[bash]
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py collectstatic --noinput
$ python3 manage.py runserver 0.0.0.0:8001
```

- Go to http://localhost:8001


