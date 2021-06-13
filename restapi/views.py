from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.conf import settings
from allauth.socialaccount.models import SocialToken, SocialAccount
<<<<<<< HEAD
#models
=======
from datetime import datetime
import json

#model imports:
>>>>>>> 85b83f186ebda63997a0c1fec6c7a34475271310
from .models import Transport, Interest, Trip, Destination, Suggestion, Like_Dislike, Company
from users.models import User

#serializer imports
from .serializers import *

<<<<<<< HEAD
#recommendation
#from recommender import reccomend
from restapi.recommender import reccomend
=======
#recommendation imports:
from restapi.recommender import reccomend
from restapi.latlong import coord_scraper
>>>>>>> 85b83f186ebda63997a0c1fec6c7a34475271310

# Create your views here.

# ------------------------------- Destination -----------------------------------#
@api_view(['GET', 'POST', ])
def destination(request):
    if request.method == 'GET':

        ## TODO: add some fields with data from the webscrapper
        d = {}
        destinations = Destination.objects.all()
        for i,dest in enumerate(destinations):
            d1 = {}

            d1["destination_id"] = dest.destination_id
            d1["trip_id"] = dest.trip_id.trip_id
            d1["name"] = dest.name
            d1["country"] = dest.country
            d1["postal_code"] = dest.postal_code
            d1["country_code"] = dest.country_code
            d1["budget"] = dest.budget

            #get the date
            if dest.date_from != None and dest.date_to != None:
                date_from = dest.date_from.strftime("%m/%d/%Y, %H:%M:%S")
                date_to = dest.date_to.strftime("%m/%d/%Y, %H:%M:%S")
            else:
                date_from = ''
                date_to = ''

            d1["date_from"] = date_from
            d1["date_to"] = date_to

            d1["n"] = dest.n
            d1["e"] = dest.e

            city = coord_scraper(dest.name, dest.country)
            city.get_image()
            d1["image"] = city.image

            weather = city.get_weather()
            d1["temperature"] = weather["temperature"]
            d1["weather_description"] = weather["description"]
            
            d[dest.destination_id] = d1

        response = json.dumps(d)
        return Response(response)

    elif request.method == 'POST':
        data = request.data
        coords = coord_scraper( data["name"], data["country"])
        coords.get_coords()

        trip = Trip.objects.get(trip_id = data["trip_id"])

        destination = Destination(trip_id=trip, postal_code=data["postal_code"], name=data["name"],
                                  country=data["country"], country_code=data["country_code"], budget=data["budget"], n=coords.lat, e=coords.lon,
                                  date_from=data["date_from"], date_to=data["date_to"])
        destination.save()

        serializer = DestinationSerializer(destination)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', ])
def get_destination_by_id(request, pk, format=None):
    if request.method == 'GET':
        dest = Destination.objects.get(destination_id=pk)
        d = {}

        d["destination_id"] = dest.destination_id
        d["trip_id"] = dest.trip_id.trip_id
        d["name"] = dest.name
        d["country"] = dest.country
        d["postal_code"] = dest.postal_code
        d["country_code"] = dest.country_code
        d["budget"] = dest.budget

        # get the date
        if dest.date_from != None and dest.date_to != None:
            date_from = dest.date_from.strftime("%m/%d/%Y, %H:%M:%S")
            date_to = dest.date_to.strftime("%m/%d/%Y, %H:%M:%S")
        else:
            date_from = ''
            date_to = ''

        d["date_from"] = date_from
        d["date_to"] = date_to

        d["n"] = dest.n
        d["e"] = dest.e

        city = coord_scraper(dest.name, dest.country)
        city.get_image()
        d["image"] = city.image
        weather = city.get_weather()
        d["temperature"] = weather["temperature"]
        d["weather_description"] = weather["description"]

        response = json.dumps(d)
        return Response(response)

@api_view(['GET', ])
def get_destination_by_trip_id(request, fk, format=None):
    if request.method == 'GET':
        dest = Destination.objects.filter(trip_id=fk)
        serializer = DestinationSerializer(dest, many=True)
        return Response(serializer.data)


# ------------------------------- Destination -----------------------------------#

# ------------------------------- Trip -----------------------------------#

@api_view(['GET', 'POST', ])
def trip(request, format=None):
    access_token = request.headers["Authorization"].split("Bearer ")[1]
    token = SocialToken.objects.get(token=access_token)
    social_acc = SocialAccount.objects.get(socialtoken=token.id)
    user = User.objects.get(id=social_acc.user.id)

    if request.method == 'GET':
        trips = Trip.objects.filter(user_id = user.id)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        request.data["user_id"] = user.id
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def get_trip_by_id(request, pk, format=None):
    if request.method == 'GET':
        trip = Trip.objects.get(trip_id=pk)
        serializer = TripSerializer(trip)
        return Response(serializer.data)


# ------------------------------- Trip -----------------------------------#

# ------------------------------- Interests -----------------------------------#
@api_view(['POST', 'GET', ])
def user_interests(request):
    access_token = request.headers["Authorization"].split("Bearer ")[1]
    token = SocialToken.objects.get(token=access_token)
    social_acc = SocialAccount.objects.get(socialtoken=token.id)
    user = User.objects.get(id=social_acc.user.id)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        for key in data:
            for value in data[key]:
                interest = Interest.objects.get(interest_id=value)
                user.interests.add(interest)

        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['GET', 'POST',])
def interests(request, format=None):
    if request.method == 'GET':
        interests = Interest.objects.all()
        serializer = InterestsSerializer(interests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InterestsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------- Interests -----------------------------------#

# ------------------------------- User -----------------------------------#

@api_view(['GET', ])
def user_info(request):
    if request.method == 'GET':
        access_token = request.headers["Authorization"].split("Bearer ")[1]
        token = SocialToken.objects.get(token=access_token)
        social_acc = SocialAccount.objects.get(socialtoken=token.id)
        user = User.objects.get(id=social_acc.user.id)

        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['POST', ])
def user_add(request):
    if request.method == 'POST':
        access_token = request.headers["Authorization"].split("Bearer ")[1]
        token = SocialToken.objects.get(token=access_token)
        social_acc = SocialAccount.objects.get(socialtoken=token.id)
        user = User.objects.get(id=social_acc.user.id)

        data = request.data
        user.age = data["age"]
        user.gender =  data["gender"]
        user.recieve_emails = data["recieve_emails"]
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)


#------------------------------- User -----------------------------------#

#------------------------------- Company -----------------------------------#

@api_view(['POST', 'GET', ])
def user_company(request, format=None):
    access_token = request.headers["Authorization"].split("Bearer ")[1]
    token = SocialToken.objects.get(token=access_token)
    social_acc = SocialAccount.objects.get(socialtoken=token.id)
    user = User.objects.get(id=social_acc.user.id)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        for key in data:
            for value in data[key]:
                company = Company.objects.get(company_id=value)
                user.company.add(company)

        serializer = UserSerializer(user)
        return Response(serializer.data)

# ------------------------------- Company -----------------------------------#

#--------------------------- Recomend endpoint /api/recommend --------------------- #
## TODO: wqtqwtqwt

def get_gender(g):
    if g == "Male":
        return 1
    elif g == "Female":
        return 2
    elif g == "Other":
        return 3

def get_companies(company):
    comp = []
    for i in company:
        comp.append(i.company)

    optionsCompany = ["Family", "Partner", "Alone", "Friends"]
    output = []
    for c in optionsCompany:
        if c in comp:
            output.append(1)
        else:
            output.append(0)
    return output

def get_interests(interests):
    optionsInterests = ["Fine Arts", "Theatre", "Literary Art", "Craft", "Photography", "Cooking", "Comedy",
                        "Trips and adventurous activities", "Entertainment", "Kids events", "Yoga", "Parties",
                        "Performances", "Sports events", "Festivals", "Workshops", "Music", "Exhibitions",
                        "Food and drink", "Health and Wellness", "Dance", "Fashion", "Arts"]

    seznam = []
    for i in interests:
        seznam.append(i.interest)

    output = []
    for i in optionsInterests:
        if i in seznam:
            output.append(1)
        else:
            output.append(0)

    return output


@api_view(['GET', ])
def get_recommendations(request, destination_id, format=None):
    if request.method == 'GET':
        destination = Destination.objects.get(destination_id=destination_id)
        city = destination.name

        access_token = request.headers["Authorization"].split("Bearer ")[1]
        token = SocialToken.objects.get(token=access_token)
        social_acc = SocialAccount.objects.get(socialtoken=token.id)
        user = User.objects.get(id=social_acc.user.id)

        seznam = []
        seznam.append(get_gender(user.gender))
        seznam.append(user.age)

        interests = get_interests(user.interests.all())
        for i in interests:
            seznam.append(i)

        companies = get_companies(user.company.all())
        for c in companies:
            seznam.append(c)

        print(seznam)
        print(city)
        data = reccomend(seznam, city)

        return Response(data)

# ------------------------------- Company -----------------------------------#

@api_view(['POST', 'GET', ])
def user_company(request, format=None):
    access_token = request.headers["Authorization"].split("Bearer ")[1]
    token = SocialToken.objects.get(token=access_token)
    social_acc = SocialAccount.objects.get(socialtoken=token.id)
    user = User.objects.get(id=social_acc.user.id)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        for key in data:
            for value in data[key]:
                company = Company.objects.get(company_id=value)
                user.company.add(company)

        serializer = UserSerializer(user)
        return Response(serializer.data)

# ------------------------------- Company -----------------------------------#

#--------------------------- Recomend endpoint /api/recommend --------------------- #
## TODO: wqtqwtqwt

def get_gender(g):
    if g == "Male":
        return 1
    elif g == "Female":
        return 2
    elif g == "Other":
        return 3

def get_companies(company):
    comp = []
    for i in company:
        comp.append(i.company)

    optionsCompany = ["Family", "Partner", "Alone", "Friends"]
    output = []
    for c in optionsCompany:
        if c in comp:
            output.append(1)
        else:
            output.append(0)
    return output

def get_interests(interests):
    optionsInterests = ["Fine Arts", "Theatre", "Literary Art", "Craft", "Photography", "Cooking", "Comedy",
                        "Trips and adventurous activities", "Entertainment", "Kids events", "Yoga", "Parties",
                        "Performances", "Sports events", "Festivals", "Workshops", "Music", "Exhibitions",
                        "Food and drink", "Health and Wellness", "Dance", "Fashion", "Arts"]

    seznam = []
    for i in interests:
        seznam.append(i.interest)

    output = []
    for i in optionsInterests:
        if i in seznam:
            output.append(1)
        else:
            output.append(0)

    return output


@api_view(['GET', ])
def get_recommendations(request, city, format=None):
    if request.method == 'GET':
        access_token = request.headers["Authorization"].split("Bearer ")[1]
        token = SocialToken.objects.get(token=access_token)
        social_acc = SocialAccount.objects.get(socialtoken=token.id)
        user = User.objects.get(id=social_acc.user.id)

        seznam = []
        seznam.append(get_gender(user.gender))
        seznam.append(user.age)

        interests = get_interests(user.interests.all())
        for i in interests:
            seznam.append(i)

        companies = get_companies(user.company.all())
        for c in companies:
            seznam.append(c)

        print("The seznam:")
        print(seznam)

        data = reccomend(seznam, city)

        return Response(data)

# ------------------------------- Tests -----------------------------------#
@api_view(['GET', 'POST',])
def interests_test(request, format=None):
    if request.method == 'GET':
        interests = Interest.objects.all()
        serializer = InterestsSerializer(interests, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        access_token = request.headers["Authorization"].split("Bearer ")[1]
        token = SocialToken.objects.get(token=access_token)
        user = SocialAccount.objects.get(socialtoken=token.id)
        return HttpResponse(user)


@api_view(['GET', ])
def get_token(request):
    access_token = request.headers["Authorization"].split("Bearer ")[1]
    token = SocialToken.objects.get(token=access_token)
    social_acc = SocialAccount.objects.get(socialtoken=token.id)
    user = User.objects.get(id=social_acc.user.id)

    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET', ])
def test_user_trip(request, user, format=None):
    if request.method == 'GET':
        batman = User.objects.get(username=user)

        trips = Trip.objects.filter(user_id=batman.pk)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

@api_view(['GET', ])
def get_user(request, id, format=None):
    if request.method == 'GET':
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['GET', ])
def get_user_token(request, token, format=None):
    if request.method == 'GET':
        user = User.objects.get(id=token)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# ------------------------------- Tests -----------------------------------#


# ------------------------------- Add Items -----------------------------------#
def add_users(request):
    user = User(username='imbatman', first_name='Bruce', last_name='Wayne', email='bat_guy@gmail.com')
    user.save()

    user = User(username='superMan', first_name='Clark', last_name='Kent', email='super_man007@gmail.com')
    user.save()

    user = User(username='spiderman', first_name='Peter', last_name='Parker', email='pajak_covek@gmail.com')
    user.save()
    return HttpResponse("Users added :)")

def add_items(request):
    transport = Transport(transport_id='1', transport_type='plane', ticket=100)
    transport.save()

    transport = Transport(transport_id='2', transport_type='plane', ticket=85)
    transport.save()

    transport = Transport(transport_id='3', transport_type='bus', ticket=60)
    transport.save()

    transport = Transport(transport_id='4', transport_type='train', ticket=40)
    transport.save()

    batman = User.objects.get(username='imbatman')
    travel = User.objects.get(username='superMan')
    spiderman = User.objects.get(username='spiderman')

    trip = Trip(user_id=batman, trip_id='1')
    trip.save()

    trip = Trip(user_id=batman, trip_id='2')
    trip.save()

    trip = Trip(user_id=batman, trip_id='3')
    trip.save()

    trip = Trip(user_id=travel, trip_id='2')
    trip.save()

    trip = Trip(user_id=travel, trip_id='4')
    trip.save()

    trip = Trip(user_id=spiderman, trip_id='1')
    trip.save()

    trip = Trip(user_id=spiderman, trip_id='4')
    trip.save()

    trip1 = Trip.objects.get(trip_id='1')
    trip2 = Trip.objects.get(trip_id='2')
    trip3 = Trip.objects.get(trip_id='3')
    trip4 = Trip.objects.get(trip_id='4')

    # date_from='2020.12.19', date_to='2020.12.29'
    destination = Destination(trip_id=trip1, destination_id='1', postal_code='1000', name='Ljubjana',
                              country="Slovenia", country_code='386', budget='600', n='1.0', e='1.0')
    destination.save()

    destination = Destination(trip_id=trip2, destination_id='2', postal_code='6000', name='Ohrid',
                              country="Macedonia", country_code='389', budget='500', n='1.0', e='1.0')
    destination.save()

    destination = Destination(trip_id=trip3, destination_id='3', postal_code='1010', name='Vienna',
                              country="Austria", country_code='43', budget='800', n='1.0', e='1.0')
    destination.save()

    destination = Destination(trip_id=trip4, destination_id='4', postal_code='9000', name='Ghent',
                              country="Belgium", country_code='32', budget='1000', n='1.0', e='1.0')
    destination.save()

    dest1 = Destination.objects.get(destination_id='1')
    dest2 = Destination.objects.get(destination_id='2')
    dest3 = Destination.objects.get(destination_id='3')
    dest4 = Destination.objects.get(destination_id='4')

    suggestion = Suggestion(destination_id=dest1, suggestion_id='1', description='Suggestion for Ljubjana!')
    suggestion.save()

    suggestion = Suggestion(destination_id=dest2, suggestion_id='2', description='Suggestion for Ohrid!')
    suggestion.save()

    suggestion = Suggestion(destination_id=dest3, suggestion_id='3', description='Suggestion for Vienna!')
    suggestion.save()

    suggestion = Suggestion(destination_id=dest4, suggestion_id='4', description='Suggestion for Ghent!')
    suggestion.save()

    sugg1 = Suggestion.objects.get(suggestion_id='1')
    sugg2 = Suggestion.objects.get(suggestion_id='2')
    sugg3 = Suggestion.objects.get(suggestion_id='3')
    sugg4 = Suggestion.objects.get(suggestion_id='4')

    like_dislike = Like_Dislike(id='1', user_id=batman, suggestion_id=sugg1, liked=True)
    like_dislike.save()

    like_dislike = Like_Dislike(id='2', user_id=batman, suggestion_id=sugg2, liked=True)
    like_dislike.save()

    like_dislike = Like_Dislike(id='3', user_id=batman, suggestion_id=sugg3, liked=True)
    like_dislike.save()

    like_dislike = Like_Dislike(id='4', user_id=travel, suggestion_id=sugg4, liked=True)
    like_dislike.save()

    like_dislike = Like_Dislike(id='5', user_id=spiderman, suggestion_id=sugg4, liked=False)
    like_dislike.save()

    return HttpResponse("Items added :)")

def add_interests(request):
    optionsInterests = ["Fine Arts", "Theatre", "Literary Art", "Craft", "Photography", "Cooking", "Comedy",
                        "Trips and adventurous activities", "Entertainment", "Kids events", "Yoga", "Parties",
                        "Performances", "Sports events", "Festivals", "Workshops", "Music", "Exhibitions",
                        "Food and drink", "Health and Wellness", "Dance", "Fashion", "Arts"]

    for i in optionsInterests:
        interest = Interest(interest=i)
        interest.save()
    return HttpResponse("Interests are added :)")

def add_company(request):
    optionsCompany = ["Family", "Partner", "Alone", "Friends"]

    for c in optionsCompany:
        company = Company(company=c)
        company.save()
    return HttpResponse("Companies are added :)")

# ------------------------------- Add Items -----------------------------------#