from csv import DictReader
import numpy
from sklearn.model_selection import train_test_split
import sklearn.linear_model
from restapi.script import get_events_info
import json


def reccomend(user, city):
    print("blabal")

    users = []
    crit = []
    crit.append("Gender")
    crit.append("Age")
    data = []
    dat = []
    
    optionsCompany = ["FAMILY", "PARTNER", "ALONE", "FRIENDS"]
    events = []
    optionsInterests = ["Fine Arts", "Theatre", "Literary Art", "Craft", "Photography", "Cooking", "Comedy",
                        "Trips and adventurous activities", "Entertainment", "Kids events", "Yoga", "Parties",
                        "Performances", "Sports events", "Festivals", "Workshops", "Music", "Exhibitions",
                        "Food and drink", "Health and Wellness", "Dance", "Fashion", "Arts"]


    reader = DictReader(open('restapi/anketa.csv', 'rt', encoding='utf-8'))
    brojac = 0
    for row in reader:
        line = []
        users.append(brojac)
        brojac += 1
        if row["Gender"] == "Male":
            line.append(1)
        if row["Gender"] == "Female":
            line.append(2)
        if row["Gender"] != "Male" and row["Gender"] != "Female":
            line.append(3)
        line.append(row["Age"])
        for interest in optionsInterests:
            if interest not in crit:
                crit.append(interest)
            if interest in row["Categories"].split(";"):
                line.append(1)
            else:
                line.append(0)
        for company in optionsCompany:
            if company not in crit:
                crit.append(company)
            if company in row["Company"].split(";"):
                line.append(1)
            else:
                line.append(0)
        for a in row:
            if a != "Gender" and a != "Age" and a != "Timestamp" and a != "Company" and a != "Categories":
                if "EVENT " + a not in crit:
                    crit.append("EVENT " + a)

                if a not in events:
                    events.append(a)
                line.append(float(row[a])/100)
        dat.append(line)

    for a in range(len(dat[0])):
        l = []
        for b in range(len(dat)):
            l.append(dat[b][a])
        data.append(l)

    data = numpy.array(data).astype(float)
    #print(data)
    sol={}
    ## TODO: give marijana vakva matrika ko dole, call the function recomend(user, "[grad nekoj]")
    nov_user = [2, 20, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1]
    ##         m/f age ##              INTERESTS                          #############  FAMILY, FRIENDS, FAMILY, PARTNER, ALONE FRIENDS
    ## 
    ##          1=m/2=f/3=other, The other 1/0 numbers are interest, 1=liked, 0=not liked
    ## 'Fine Arts', 'Theatre', 'Literary Art', 'Craft', 'Photography', 'Cooking', 'Comedy', 'Trips and adventurous activities', 'Entertainment', 'Kids events', 'Yoga', 'Parties', 'Performances', 'Sports events', 'Festivals', 'Workshops', 'Music', 'Exhibitions', 'Food and drink', 'Health and Wellness', 'Dance', 'Fashion', 'Arts'
    x = data
    y = user
    r = sklearn.linear_model.RidgeCV([0.1, 1, 10, 100])
    xtr, xte, = train_test_split(x, test_size=23)
    r.fit(xtr, y)
    pr = r.predict(xte)
    for a in range(len(pr)):
        sol[events[a]]=pr[a]
    sol =dict(sorted(sol.items(), key=lambda item: item[1], reverse=True))
    searchQ={}
    for a in sol:
        pom=get_events_info(city, a)
        if pom == "Nisto":
            continue
        searchQ[len(searchQ)]=pom
        if len(searchQ)==10:
            break

    rez=json.dumps(searchQ)

    return searchQ