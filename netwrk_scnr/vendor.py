import requests
import json
import re
api = "https://api.macvendors.com/"


def Showvendor(): # use to show list
       """
         with open('devices.json') as data:
            json_data = json.load(data)  
            if isinstance(json_data, list):  
                macs = [item['mac'] for item in json_data]  
                print(macs)
                return macs  
            else:
                mac = json_data['mac']  
                print(mac)
                return mac
            """ # use this if you want to show saved details and select a MAC
       
def Validmac(mac):
    mac_regex = r'^(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})$'
    if re.fullmatch(mac_regex, mac):
        return True
    else:
        return False
    
def GetVendor(mac):
      try:
        url = f"{api}/{mac}"
        if Validmac(mac=mac):
            rdst = requests.get(url)
            print(rdst.text)  
      except Exception as e:
            print(f"ERROR {e}")
           
    






     


        
