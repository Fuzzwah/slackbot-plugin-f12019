#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import dateutil.parser
from peewee import *

db_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "formula1.sqlite")
db = SqliteDatabase(db_file)


class BaseModel(Model):
    class Meta:
        database = db


class Events(BaseModel):
    name = TextField(unique=True)
    city = TextField()
    race = DateTimeField()
    qual = DateTimeField()

db.connect()

if not Events.table_exists():
    db.create_tables([Events,], safe=True)
    races = [
                {
                    "name": "Australian Grand Prix",
                    "city": "Melbourne",
                    "race": "2019-03-17T16:10:00+1000",
                    "qual": "2019-03-16T17:00:00+1000"
                },
                {
                    "name": "Bahrain Grand Prix",
                    "city": "Sakhir",
                    "race": "2019-04-01T02:10:00+1000",
                    "qual": "2019-03-31T02:00:00+1000"
                },
                {
                    "name": "Chinese Grand Prix",
                    "city": "Shanghai",
                    "race": "2019-04-14T16:10:00+1000",
                    "qual": "2019-04-13T16:00:00+1000"
                },
                {
                    "name": "Azerbaijan Grand Prix",
                    "city": "Baku",
                    "race": "2019-04-28T22:10:00+1000",
                    "qual": "2019-04-27T23:00:00+1000"
                },
                {
                    "name": "Spanish Grand Prix",
                    "city": "Catalunya",
                    "race": "2019-05-12T23:10:00+1000",
                    "qual": "2019-05-11T23:00:00+1000"
                },
                {
                    "name": "Monaco Grand Prix",
                    "city": "Monte Carlo",
                    "race": "2019-05-26T23:10:00+1000",
                    "qual": "2019-05-25T23:00:00+1000"
                },
                {
                    "name": "Canadian Grand Prix",
                    "city": "Montreal",
                    "race": "2019-06-10T04:10:00+1000",
                    "qual": "2019-06-09T04:00:00+1000"
                },
                {
                    "name": "French Grand Prix",
                    "city": "Paul Ricard",
                    "race": "2019-06-23T23:10:00+1000",
                    "qual": "2019-06-22T23:00:00+1000"
                },
                {
                    "name": "Austrian Grand Prix",
                    "city": "Spielberg",
                    "race": "2019-06-30T23:10:00+1000",
                    "qual": "2019-06-29T23:00:00+1000"
                },
                {
                    "name": "British Grand Prix",
                    "city": "Silverstone",
                    "race": "2019-07-14T23:10:00+1000",
                    "qual": "2019-07-13T23:00:00+1000"
                },
                {
                    "name": "German Grand Prix",
                    "city": "Hockenheim",
                    "race": "2019-07-28T23:10:00+1000",
                    "qual": "2019-07-27T23:00:00+1000"
                },
                {
                    "name": "Hungarian Grand Prix",
                    "city": "Budapest",
                    "race": "2019-08-04T23:10:00+1000",
                    "qual": "2019-08-03T23:00:00+1000"
                },
                {
                    "name": "Belgian Grand Prix",
                    "city": "Spa-Francorchamps",
                    "race": "2019-09-01T23:10:00+1000",
                    "qual": "2019-08-31T23:00:00+1000"
                },
                {
                    "name": "Italian Grand Prix",
                    "city": "Monza",
                    "race": "2019-09-08T23:10:00+1000",
                    "qual": "2019-09-07T23:00:00+1000"
                },
                {
                    "name": "Singapore Grand Prix",
                    "city": "Singapore",
                    "race": "2019-09-22T22:10:00+1000",
                    "qual": "2019-09-21T23:00:00+1000"
                },
                {
                    "name": "Russian Grand Prix",
                    "city": "Sochi",
                    "race": "2019-09-29T21:10:00+1000",
                    "qual": "2019-09-28T22:00:00+1000"
                },
                {
                    "name": "Japanese Grand Prix",
                    "city": "Suzuka",
                    "race": "2019-10-13T16:10:00+1000",
                    "qual": "2019-10-12T17:00:00+1000"
                },
                {
                    "name": "Mexican Grand Prix",
                    "city": "Mexico City",
                    "race": "2019-10-28T06:10:00+1000",
                    "qual": "2019-10-27T05:00:00+1000"
                },
                {
                    "name": "United States Grand Prix",
                    "city": "Austin",
                    "race": "2019-11-04T06:10:00+1000",
                    "qual": "2019-11-03T08:00:00+1000"
                },
                {
                    "name": "Brazilian Grand Prix",
                    "city": "Sao Paulo",
                    "race": "2019-11-18T05:10:00+1000",
                    "qual": "2019-11-17T05:00:00+1000"
                },
                {
                    "name": "Abu Dhabi Grand Prix",
                    "city": "Yas Marina",
                    "race": "2019-12-02T00:10:00+1000",
                    "qual": "2019-12-01T00:00:00+1000"
                },
                {
                    "name": "Australian Grand Prix",
                    "city": "Melbourne",
                    "race": "2020-03-15T16:10:00+1000",
                    "qual": "2020-03-14T17:00:00+1000"
                },                
            ]
    for race in races:
        print(race)
        race_datetime = dateutil.parser.parse(race['race'])
        qual_datetime = dateutil.parser.parse(race['qual'])
        
        g = Events(name=race['name'],city=race['city'],race=race_datetime,qual=qual_datetime)
        g.save()
