import requests
import json
from time import sleep
import threading 

with open('settings.json', 'r') as f:
    data = json.load(f)

delayms = int(data["delayms"]) / 1000
webhookurl = data["webhook"]
send_webhook_on_startup = data["sendWebhookOnStartup"]

headers = {
    "accept": "*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://www.post.at",
    "pragma": "no-cache",
    "referer": "https://www.post.at/",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

def webhook(json):
  deliver = ""
  country = ""
  try:
      deliver = json["data"]["einzelsendung"]["estimatedDelivery"]["startDate"]
  except:
      deliver = " - "
  try:
      country = ":flag_"+(json["data"]["einzelsendung"]["sendungsEvents"][len(json["data"]["einzelsendung"]["sendungsEvents"])-1]["eventcountry"]).lower()+":"
  except:
      country = " - "
  payload = {
    "content": None,
    "embeds": [
      {
        "title": json["data"]["einzelsendung"]["sendungsnummer"],
        "url": "https://www.post.at/s/sendungsdetails?snr="+json["data"]["einzelsendung"]["sendungsnummer"],
        "color": None,
        "fields": [
          {
            "name": "weight",
            "value": str(json["data"]["einzelsendung"]["weight"]),
            "inline": True
          },
          {
            "name": "estimated delivery",
            "value": deliver,
            "inline": True
          },
          {
            "name": "Event",
            "value": json["data"]["einzelsendung"]["sendungsEvents"][len(json["data"]["einzelsendung"]["sendungsEvents"])-1]["text"],
            "inline": True
          },
          {
            "name": "Event-Country",
            "value": country,
            "inline": True
          },
          {
            "name": "Event-ZIP",
            "value": json["data"]["einzelsendung"]["sendungsEvents"][len(json["data"]["einzelsendung"]["sendungsEvents"])-1]["eventpostalcode"],
            "inline": True
          },
          {
            "name": "Timestamp",
            "value": json["data"]["einzelsendung"]["sendungsEvents"][len(json["data"]["einzelsendung"]["sendungsEvents"])-1]["timestamp"]
          }
        ],
        "author": {
          "name": "New Event found!"
        },
        "footer": {
          "text": "0felix000 - ATPost Shipment Tracker"
        }
      }
    ],
    "attachments": []
  }
  r = requests.post(webhookurl, json = payload)
def track(number, dummy):
    x = 0
    oldlen = -1
    first = True
    while x == 0:
        print(number + " | Requesting tracking endpoint...")
        payload = {"query":"query {\n        einzelsendung(sendungsnummer: \""+number+"\") {\n          sendungsnummer\n          branchkey\n          estimatedDelivery {\n            startDate\n            endDate\n            startTime\n            endTime\n          }\n          dimensions {\n            height\n            width\n            length\n          }\n          status\n          weight\n          sendungsEvents {\n            timestamp\n            status\n            reasontypecode\n            text\n            textEn\n            eventpostalcode\n            eventcountry\n          }\n          customsInformation {\n            customsDocumentAvailable,\n            userDocumentNeeded\n          }\n        }\n      }"}
        r = requests.post("https://api.post.at/sendungen/sv/graphqlPublic", headers = headers, json = payload)
        j = json.loads(r.text)
        if first == True:
            if j["data"]["einzelsendung"] == None:
                print(number  + " | Shipment not found.")
                return
            print(number + " | Found shipment!")
        events = j["data"]["einzelsendung"]["sendungsEvents"]
        last = events[len(events)-1]
        print(number + " | Status: " + last["text"])
        if first == True and send_webhook_on_startup == True:
            webhook(j)
        elif len(events) != oldlen and first == False:
            webhook(j)
            
        first = False
        oldlen = len(events)
        sleep(delayms)
        if "zugestellt" in last["text"]:
            return
        
with open("numbers.txt", "r") as file:
    for line in file:
        l = line.strip()
        threading.Thread(target=track, args=(l,"")).start()

input()