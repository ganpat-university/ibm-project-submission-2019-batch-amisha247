import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from geopy.geocoders import Nominatim
import pymongo



myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DrowningPep"]
city_mongo = mydb["city"]


geolocator = Nominatim(user_agent="MyApp")



response = requests.get("https://www.adda247.com/defence-jobs/indian-cities-on-river-banks/")
soup = BeautifulSoup(response.content, "html.parser")
rows = soup.find_all("tr")
data = []


for row in rows:
	cells = row.find_all("td")
	data.append([cell.text for cell in cells])

df = pd.DataFrame(data)
df = df.replace(r'\n',' ', regex=True)
first_df = df.head(1)

json_data = {
	"data":[]	
}



i=0
for x in df.values.tolist():
	tmp=[]
	for y in x:
		tmp.append( ((y.replace("\n",""))).replace("\xa0"," ") )

	if i!=0:
		json_data["data"].append( tmp )
	i=i+1



new_json_with_let_lng = {
	"data":[]
}

for x in json_data['data']:
	if x[0]!=" Thiruchirapalli ":
		location = geolocator.geocode( x[0]+" ,"+x[-1] )
	
		x.append(location.latitude)
		x.append(location.longitude)

		new_json_with_let_lng['data'].append( x )


fin_lst = []

for x in new_json_with_let_lng["data"]:
	city = x[0]
	river = x[1]
	state = x[2]
	lat = x[3]
	lon = x[4]

	tmp_json = {"city":city,"river":river,"state":state,"lat":lat,"lon":lon}
	fin_lst.append(tmp_json)

print(fin_lst)

# jArray = json.dumps(fin_lst, default=json_util.default)

city_mongo.insert_many(fin_lst)