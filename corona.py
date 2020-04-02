#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 2020 e1z0 (https://github.com/e1z0)
import os
import time
import argparse as ap
from rrdtool import update as rrd_update
import rrdtool
import redis
import datetime
import json
import requests

# SOME SETTINGS
api = 'https://corona.lmao.ninja/countries/'
country = 'LT'
html_dir = '/var/www/html/corona/'
report_telegram = 1
tg_bot = "create_bot_and_copy_text_after_bot_string"
tg_chatid = "chat_id"
##############

def ReadApiData():
 resp = requests.get(url=api+country)
 if (report_telegram > 0):
   r = redis.Redis()
   if (r.exists("last_corona")):
       last_data = json.loads(r.get("last_corona"))
       new_data = resp.json()
       if (last_data['cases'] != new_data['cases']):
         cases = (new_data['cases']-last_data['cases'])
         TelegramNotification("We have new corona cases: "+str(cases)+" today total cases in our country: "+str(new_data['todayCases']))
   else:
       print("There is no data about corona in redis backend, setting one. :)")
   r.set("last_corona",resp.content)
 return resp.json()

def TelegramNotification(text):
 payload = {
            'chat_id': tg_chatid,
            'text': text,
            'parse_mode': 'HTML'
        }
 return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=tg_bot),data=payload).content

def JustRead():
 data = ReadApiData()
 print ("Today cases: "+str(data['todayCases']))
 print ("Today deaths: "+str(data['todayDeaths']))
 print ("--------------------------------")
 print ("Current cases: "+str(data['cases']))
 print ("Active cases: "+str(data['active']))
 print ("Critical: "+str(data['critical']))
 print ("Recovered: "+str(data['deaths']))

def Initialize():
 print ("I should do some initialization here")
 ret = rrdtool.create("corona.rrd", "--step", "300", "--start", '0',
 "DS:todaycases:GAUGE:172800:0:U",
 "DS:todaydeaths:GAUGE:172800:0:U",
 "DS:cases:GAUGE:172800:0:U",
 "DS:active:GAUGE:172800:0:U",
 "DS:critical:GAUGE:172800:0:U",
 "DS:recovered:GAUGE:172800:0:U",
 "DS:deaths:GAUGE:172800:0:U",
 "RRA:AVERAGE:0.5:1:288",
 "RRA:AVERAGE:0.5:3:672",
 "RRA:AVERAGE:0.5:12:744",
 "RRA:AVERAGE:0.5:72:1460",
 "RRA:MIN:0.5:1:288",
 "RRA:MIN:0.5:3:672",
 "RRA:MIN:0.5:12:744",
 "RRA:MIN:0.5:72:1460",
 "RRA:MAX:0.5:1:288",
 "RRA:MAX:0.5:3:672",
 "RRA:MAX:0.5:12:744",
 "RRA:MAX:0.5:72:1460")

def Graph():
 print ("Generating graphs")
 for sched in ['daily' , 'weekly', 'monthly']:
    if sched == 'weekly':
        period = 'w'
    elif sched == 'daily':
        period = 'd'
    elif sched == 'monthly':
        period = 'm'
    ret = rrdtool.graph( html_dir+"metrics-%s.png" %(sched), "--start", "-1%s" %(period), "--vertical-label=Virus statistics",
         '--watermark=Corona',
         "-w 800",
         "DEF:todaycases=corona.rrd:todaycases:AVERAGE",
         "DEF:todaydeaths=corona.rrd:todaydeaths:AVERAGE",
         "DEF:cases=corona.rrd:cases:AVERAGE",
         "DEF:active=corona.rrd:active:AVERAGE",
         "DEF:critical=corona.rrd:critical:AVERAGE",
         "DEF:recovered=corona.rrd:recovered:AVERAGE",
         "DEF:deaths=corona.rrd:deaths:AVERAGE",
         "AREA:cases#8ADCFF:Cases",
         "GPRINT:cases:LAST:        Now\:%8.2lf %s",
         "GPRINT:cases:MIN:Min\:%8.2lf %s",
         "GPRINT:cases:AVERAGE:Avg\:%8.2lf %s",
         "GPRINT:cases:MAX:Max\:%8.2lf %s\\n",
         "LINE1:todaycases#D7D76C:Cases today",
         "GPRINT:todaycases:LAST:  Now\:%8.2lf %s",
         "GPRINT:todaycases:MIN:Min\:%8.2lf %s",
         "GPRINT:todaycases:AVERAGE:Avg\:%8.2lf %s",
         "GPRINT:todaycases:MAX:Max\:%8.2lf %s\\n",
         "LINE2:todaydeaths#E73B19:Deaths today",
         "GPRINT:todaydeaths:LAST:     Now\:%8.2lf %s",
         "GPRINT:todaydeaths:MIN:Min\:%8.2lf %s",
         "GPRINT:todaydeaths:AVERAGE:Avg\:%8.2lf %s",
         "GPRINT:todaydeaths:MAX:Max\:%8.2lf %s\\n",
         "LINE3:active#DBE719:Active ill",
         "GPRINT:active:LAST:    Now\:%8.2lf %s",
         "GPRINT:active:MIN:Min\:%8.2lf %s",
         "GPRINT:active:AVERAGE:Avg\:%8.2lf %s",
         "GPRINT:active:MAX:Max\:%8.2lf %s\\n",
         "LINE4:critical#A4A498:Critical",
         "GPRINT:critical:LAST:   Now\:%8.2lf %s",
         "GPRINT:critical:MIN:Min\:%8.2lf %s",
         "GPRINT:critical:AVERAGE:Avg\:%8.2lf %s",
         "GPRINT:critical:MAX:Max\:%8.2lf %s\\n",
         "LINE5:recovered#23A92F:Recovered",
         "GPRINT:recovered:LAST:          Now\:%8.2lf %s",
         "GPRINT:recovered:MIN:Min\:%8.2lf %s",
         "GPRINT:recovered:AVERAGE:Avg\:%8.2lf %s",
         "GPRINT:recovered:MAX:Max\:%8.2lf %s\\n",
         "LINE6:deaths#F0210C:Deaths",
         "GPRINT:deaths:LAST:              Now\:%8.2lf %s",
         "GPRINT:deaths:MIN:Min\:%8.2lf %s",
         "GPRINT:deaths:AVERAGE:Avg\:%8.2lf %s",
         "GPRINT:deaths:MAX:Max\:%8.2lf %s\\n")

def UpdateRRD():
 print ("Updating rrdtool database")
 data = ReadApiData()
 ret = rrd_update('corona.rrd', 'N:%s:%s:%s:%s:%s:%s:%s' %(data['todayCases'], data['todayDeaths'], data['cases'], data['active'], data['critical'], data['recovered'], data['deaths']));

os.chdir(os.path.dirname(__file__))
parser = ap.ArgumentParser(description="Show corona stats per country or generate old school rrdtool based cool graphs :)")
parser.add_argument('--initialize', help='Initialize rrdtool database file',action='store_true')
parser.add_argument('--graph', help='Write cool graph',action='store_true')
parser.add_argument('--update', help='Update RRD database',action='store_true')
args = parser.parse_args()
if args.graph is True:
 Graph()
elif args.update is True:
 UpdateRRD()
elif args.initialize is True:
 Initialize()
else:
 JustRead()
