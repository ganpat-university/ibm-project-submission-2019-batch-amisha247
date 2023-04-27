import requests
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DrowningPep"]
city_mongo = mydb["city"]


f = open("key.txt", "r")
api_url1 = "https://api.openweathermap.org/data/2.5/weather?lat="
api_url2 = "&lon="
api_url3 = "&appid="
api_key = f.read()


city_data = city_mongo.find()
tot_val = 0
for y in city_data:
	tot_val=tot_val+1
print("Total Citys are "+str(tot_val))

city_data = city_mongo.find()
for x in city_data:
	api_url = api_url1+str(x['lat'])+api_url2+str(x['lon'])+api_url3+api_key
	response = requests.get(api_url)
	print(response)
	print(api_url)
	if str(response) == "<Response [200]>":
		myquery = { "_id": x['_id'] }
		newvalues = { "$set": { "api_data": response.json() } }
		city_mongo.update_many(myquery, newvalues)
		print("complited value is "+str(tot_val))
		tot_val = tot_val - 1
		print()
