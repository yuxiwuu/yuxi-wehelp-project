import urllib.request as request
import json
url_ch="https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
url_en="https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
with request.urlopen(url_ch) as response:
    data_ch=json.load(response)
with request.urlopen(url_en) as response:
    data_en=json.load(response)

ch_list=data_ch["list"]
en_list=data_en["list"]

en_dict={}
for item in en_list:
    phone = item["tel"]
    en_dict[phone] = item

import csv
import re
with open("hotels.csv", mode="w",newline="", encoding="utf-8") as file:
    writer=csv.writer(file)
    for ch_item in ch_list:
        ch_name = ch_item["旅宿名稱"]
        ch_address = ch_item["地址"].replace("臺北市", "").replace("台北市", "")
        ch_phone = ch_item["電話或手機號碼"].strip()
        ch_rooms = ch_item["房間數"]

        if ch_phone in en_dict:
            en_item = en_dict[ch_phone]
            en_name = en_item["hotel name"]
            en_address = en_item["address"]

            en_address = re.split(r"Taipei", en_address)[0]
            en_address = en_address.strip().rstrip(",")

        writer.writerow([ch_name,en_name,ch_address,en_address,ch_phone,ch_rooms])

import csv
districts={}
for hotel in ch_list:
    address=hotel["地址"]
    rooms=int(hotel["房間數"])
    DistrictName=address[3:6]
    if DistrictName not in districts:
       districts[DistrictName]={"HotelCount":0,"RoomCount":0}
    districts[DistrictName]["HotelCount"] += 1
    districts[DistrictName]["RoomCount"] += rooms

with open("districts.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for dist in districts:
        writer.writerow([dist,districts[dist]["HotelCount"],districts[dist]["RoomCount"]])