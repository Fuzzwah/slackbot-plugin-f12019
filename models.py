#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import dateutil.parser
from peewee import *

db_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "f1.sqlite")
db = SqliteDatabase(db_file)


class BaseModel(Model):
    class Meta:
        database = db


class Season2019(BaseModel):
    name = TextField(unique=True)
    city = TextField()
    datetime = DateTimeField()

db.connect()

if not Season2019.table_exists():
    db.create_tables([Season2019,], safe=True)
    races = [{
                "name": "Australian Grand Prix",
                "city": "Melbourne",
                "date": "2019-03-17",
                "time": "16:10"
            },
            {
                "name": "Bahrain Grand Prix",
                "city": "Sakhir",
                "date": "2019-04-01",
                "time": "02:10"
            },
            {
                "name": "Chinese Grand Prix",
                "city": "Shanghai",
                "date": "2019-04-14",
                "time": "16:10"
            },
            {
                "name": "Azerbaijan Grand Prix",
                "city": "Baku",
                "date": "2019-04-28",
                "time": "22:10"
            },
            {
                "name": "Spanish Grand Prix",
                "city": "Catalunya",
                "date": "2019-05-12",
                "time": "23:10"
            },
            {
                "name": "Monaco Grand Prix",
                "city": "Monte Carlo",
                "date": "2019-05-26",
                "time": "23:10"
            },
            {
                "name": "Canadian Grand Prix",
                "city": "Montreal",
                "date": "2019-06-10",
                "time": "04:10"
            },
            {
                "name": "French Grand Prix",
                "city": "Paul Ricard",
                "date": "2019-06-23",
                "time": "23:10"
            },
            {
                "name": "Austrian Grand Prix",
                "city": "Spielberg",
                "date": "2019-06-30",
                "time": "23:10"
            },
            {
                "name": "British Grand Prix",
                "city": "Silverstone",
                "date": "2019-07-14",
                "time": "23:10"
            },
            {
                "name": "German Grand Prix",
                "city": "Hockenheim",
                "date": "2019-07-28",
                "time": "23:10"
            },
            {
                "name": "Hungarian Grand Prix",
                "city": "Budapest",
                "date": "2019-08-04",
                "time": "23:10"
            },
            {
                "name": "Belgian Grand Prix",
                "city": "Spa-Francorchamps",
                "date": "2019-09-01",
                "time": "23:10"
            },
            {
                "name": "Italian Grand Prix",
                "city": "Monza",
                "date": "2019-09-08",
                "time": "23:10"
            },
            {
                "name": "Singapore Grand Prix",
                "city": "Singapore",
                "date": "2019-09-22",
                "time": "22:10"
            },
            {
                "name": "Russian Grand Prix",
                "city": "Sochi",
                "date": "2019-09-29",
                "time": "21:10"
            },
            {
                "name": "Japanese Grand Prix",
                "city": "Suzuka",
                "date": "2019-10-13",
                "time": "16:10"
            },
            {
                "name": "Mexican Grand Prix",
                "city": "Mexico city",
                "date": "2019-10-28",
                "time": "06:10"
            },
            {
                "name": "United States Grand Prix",
                "city": "Austin",
                "date": "2019-11-04",
                "time": "06:10"
            },
            {
                "name": "Brazilian Grand Prix",
                "city": "Sao Paulo",
                "date": "2019-11-18",
                "time": "05:10"
            },
            {
                "name": "Abu Dhabi Grand Prix",
                "city": "Yas Marina",
                "date": "2019-12-02",
                "time": "00:10"
            }]
    for race in races:
        print(race)
        datetime = dateutil.parser.parse('{}T{}:00+10:00'.format(race['date'], race['time']))
        g = Season2019(name=race['name'],city=race['city'],datetime=datetime)
        g.save()
