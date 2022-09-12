import requests.auth
import requests
import datetime
import json
import src.creds


url = "https://api.eu.opsgenie.com/v2/alerts"
headers = {"Authorization": "GenieKey acc0c3fc-13d8-4b3c-af0a-2cbd136e38b8"}
#auth = requests.auth('Authorization: GenieKey eb243592-faa2-4ba2-a551q-1afdf565c889')
req = requests.get(url, headers=headers)
print(req.json())

def test():
    url = "https://api.eu.opsgenie.com/v2/alerts"
    headers = {"Authorization": src.creds.api_key}
    # auth = requests.auth('Authorization: GenieKey eb243592-faa2-4ba2-a551q-1afdf565c889')
    notification = {
            "source": "Kraken Price Changes",
            "message": "Test",
            "sent_timestamp": json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
        }
    req = requests.post(url, headers=headers, json=notification)
    print(req.json())

test()