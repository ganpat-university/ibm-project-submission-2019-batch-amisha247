import pymongo
from bson import json_util
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DrowningPep"]
city_mongo = mydb["city"]