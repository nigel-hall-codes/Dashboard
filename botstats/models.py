from peewee import *

db = SqliteDatabase("/home/nhall/BOTvenv2/bots/trades.db")
settingsdb = SqliteDatabase("/home/nhall/BOTvenv2/bots/BotSettings.db")


class Trade(Model):

    bot_name = TextField()
    entry_time = DateTimeField()
    exit_time = DateTimeField()
    entry_price = FloatField()
    exit_price = FloatField()
    trade_size = FloatField()


    class Meta:
        database = db

class Bot(Model):
    id = PrimaryKeyField()
    name = CharField()

    class Meta:
        database = settingsdb

class BotSettings(Model):
    id = IntegerField()
    pid = IntegerField(default=0)
    bot_live = BooleanField(default=False)
    allocation = FloatField(default=0)


    class Meta:
        database = settingsdb


def initialize():
    db.connect()
    db.create_tables([Trade])


initialize()