import requests
import json
from datetime import datetime, timedelta
import os

now = datetime.now() 
today = now.strftime("%Y-%m-%d")
yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d") #new files not added often so increase the days number in timedelta to avoid empty string

#search page url:
url = "https://public-search.emploi.belgique.be/website-service/joint-work-convention/search"

#download page that will be added to each document name to have a full downloadable link
dl_url = "https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/"

#request
r = requests.post(url,json={"signatureDate": {'start': yesterday+"T00:00:00.000Z", 'end': today+"T00:00:00.000Z"}})

# If you want to filter on a specific CP (here 200), instead of dates. Both dates and CP filters can also be combined in the 'json' dict parameter
#r = requests.post(url,json={"jc":"2000000"})

data = r.json()

#function that checks if json file already exists
def where_json(file_name):
    return os.path.exists(file_name)

#checking json file and opening it if it exists
if where_json("data.json"):
    with open("data.json","r") as file:
        existing_data = json.loads(file.read())
else: #creating an empty list
    existing_data = []

new_data = []
for item in data:


    #checks if entry already existing in database
    if not any(d['depositNumber'] == item['depositNumber'] for d in existing_data):
        split = item['documentLink'].split('/')

        #gets the Commission Paritaire number
        item['CPnumber'] = split[0]

        #gets the file number
        item['DocNumber'] = split[1][:-4]

        #replaces name of the file with complete downloadable link
        item['documentLink'] = dl_url + item['documentLink']

        #downloads the pdf from link
        response = requests.get(item['documentLink'])
        if response.status_code == 200:

            #saves the pdf in directory depending on CP number
            if not os.path.exists(f"{item['CPnumber']}"):      
                os.makedirs(f"{item['CPnumber']}")

            file_path = os.path.join(f"{item['CPnumber']}",os.path.basename(item['documentLink']))

            with open(file_path, 'wb') as f:
                f.write(response.content)

        #append item data dict to list
        new_data.append(item)

        #add email alert here??? with download link?
    
    #replaces the previous existing data with new data
    if new_data: 
        existing_data = new_data

#save list as json file
json_object = json.dumps(existing_data, indent=4)

with open("data.json", "w") as outfile:
    outfile.write(json_object)

    """
    from algoliasearch.search_client import SearchClient

client = SearchClient.create('QVBA9ZZPRA', '520ea8dd3ca37da55f2c5d86729b23a8')
index = client.init_index('KPMG_index')
# record = {"objectID": "200-2022-009993"}
# results = index.search(record)
res = index.get_object("200-2022-009993")
print(res["content"][0])
"""