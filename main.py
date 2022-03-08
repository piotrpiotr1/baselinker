import requests
import json
import re

url = 'https://api.baselinker.com/connector.php'

headers = {'x-bltoken': '',

           }

data = {
    "method": "getInventoryProductsList",
    'parameters': json.dumps({"inventory_id": "905", "filter_ean": "000642"})
}

response = requests.post(url, data=data, headers=headers)

json_data = json.loads(response.text)
print(json_data)
b = re.sub("\D", "", str(json_data['products'].keys()))
print(b)




