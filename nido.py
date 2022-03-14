


import requests
import json
import xml.etree.ElementTree as ET
import re
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("urls")
url_baseliner = 'https://api.baselinker.com/connector.php'
url_feed = ''

headers_baselinker = {'x-bltoken': ''}
headers_url = {'user-agent': 'my-app/0.0.1'}

r = requests.get(url_feed, headers=headers_url)
root = ET.fromstring(r.content)
#print(r.content)


def main():

    #scrap feed xml
    for item in root.findall('o'):
        price = item.get('price')
        stock = item.get('stock')
        #sometimes a field stock disappears in a  feed file
        if(stock is None):
            stock = '0'
        name = item.find('name').text
        #name = namefull.split(' | ')[0]
        #scrap ean
        #print(price,stock,name)

        
        
        for ean in item.findall("./attrs/a[@name='EAN']"):
            ean = ean.text
            #print(ean)
            #check if product exist in baselinker by ean filter
            

            askForProduct = {
                "method": "getInventoryProductsList",
                'parameters': json.dumps({"inventory_id": "3096", "filter_ean": ean})
            }

            checkifproductexist = requests.post(url_baseliner, data=askForProduct, headers=headers_baselinker)
            json_data = json.loads(checkifproductexist.text)
            log.info(f"Baselinker response {json_data}")
            #extract product id
            productid = re.sub("\D", "", str(json_data['products'].keys()))

            #check if product exist
            if productid == "":
                #if not add to baselinker
                addProduct = {
                    "method": "addInventoryProduct",
                    'parameters': json.dumps({
                        "inventory_id": '3096',
                        "product_id": "",
                        "ean": ean,
                        "prices": {"825": price},
                        "stock": {"bl_3998": stock},
                        "locations": "bl_3998",
                        "text_fields": {
                            "name": name
                        }
                    })
                }
                requests.post(url_baseliner, data=addProduct, headers=headers_baselinker)
                log.info(f">Add to baselinker: {addProduct}")
            else:
                #if product exist update price and stock
                updateProduct = {
                    "method": "addInventoryProduct",
                    'parameters': json.dumps({
                        "inventory_id": '3096',
                        "product_id": productid,
                        "stock": {"bl_3998": stock},
                        "prices": {"825": price},
                        "locations": "bl_3998",
                    })
                }
                requests.post(url_baseliner, data=updateProduct, headers=headers_baselinker)
                log.info(f">Update in baselinker: {updateProduct}")


main()

