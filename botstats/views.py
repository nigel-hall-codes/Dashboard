from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import *
import json
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import pandas as pd


# Create your views here.

def pwToJSON(model):
    jsonObj = []
    for x in model:
        dictObj = {}
        dictObj['bot_name'] = x.bot_name
        dictObj['entry_time'] = x.entry_time
        dictObj['exit_time'] = x.exit_time
        dictObj['entry_price'] = x.entry_price
        dictObj['exit_price'] = x.exit_price
        dictObj['trade_size'] = x.trade_size

        jsonObj.append(dictObj)
    return jsonObj

def home(request):
    return render(request, 'home.html')

def live_bots():
    return models.BotSettings.select().where(models.BotSettings.bot_live == 1)

def get_stats(bot_name, timeperiod):

    timeperiods = {"Day": 1, "Week": 7, "Month": 30, "Year": 365}
    if timeperiod != "All Time":
        from_date = datetime.datetime.today() - datetime.timedelta(days=timeperiods[timeperiod])
        trades = models.Trade.select().where((models.Trade.bot_name == bot_name) & (models.Trade.entry_time > from_date))
    else:
        trades = models.Trade.select().where(models.Trade.bot_name == bot_name)


    df = pd.DataFrame(list(trades.dicts()))
    if not df.empty:

        df['return'] = df['exit_price'] / df['entry_price'] - 1 - .0015
        average_return = "%.2f%%" % (df['return'].mean() * 100)
        df['total_gain'] = df['trade_size'] * df['return']
        total_gains = "$%.2f" % df['total_gain'].sum()
        total_trades = df.shape[0]
        print(df)
        return average_return, total_gains, total_trades
    else:
        return 0, 0, 0


class BotStats(APIView):

    def get(self, request):
        trades = models.Trade.select().where(models.Trade.entry_time > datetime.datetime.now() - datetime.timedelta(days=14))
        json_obj = {}
        json_obj['bot_stats'] = pwToJSON(trades)
        print(dict(tuple(pd.DataFrame(json_obj['bot_stats']).groupby('bot_name'))))
        trades = dict(tuple(pd.DataFrame(json_obj['bot_stats']).groupby('bot_name')))
        return Response(trades)

    def post(self, request):
        data = request.data
        print(data)
        bots = live_bots()
        return_json = []
        for b in bots:
            bot_name = models.Bot.get(id=b.id).name

            print(bot_name)
            avg_return, total_gains, total_trades = get_stats(bot_name, data['timeperiod'])
            return_json.append({"bot": bot_name,
                                "total_return": total_gains,
                                "average_return": avg_return,
                                "total_trades": total_trades,
                                "trade_size": b.allocation})

        return Response(return_json)



