import pyscreenshot as ImageGrab
import numpy as np
from PIL import Image
import sys
import pyscreenshot as ImageGrab
import pyocr
import pyocr.builders
import time
import os
import webbrowser



tools = pyocr.get_available_tools()
# The tools are returned in the recommended order of usage
tool = tools[0]
#print (tools)


langs = tool.get_available_languages()
print (langs)
lang = langs[1]





#fonction de capture decran
def screengrab2():
    boxt = (209, 600, 280, 638)
    imt = ImageGrab.grab(boxt)
    file_adress = '/home/jphe/PycharmProjects/Captures/total' + str(int(time.time())) + '.png'
    imt.save(file_adress, 'PNG')
    return file_adress

def screengrab3():
    boxt = (148, 752, 364, 824)
    imt = ImageGrab.grab(boxt)
    file_adress = '/home/jphe/PycharmProjects/Captures/position' + str(int(time.time())) + '.png'
    imt.save(file_adress, 'PNG')
    return file_adress

url='https://www.virtualregatta.com/fr/offshore-jeu/'

webbrowser.open(url)
os.system("xte 'sleep 12'")                                 # pause 12 s

#os.system("xte 'mousemove 1507 849' 'mouseclick 2'")
os.system("xte 'mousemove 690 570' 'mouseclick 2'")
os.system("xte 'sleep 10'")
os.system("xte 'mousemove 1507 849' 'mouseclick 2'")        # mise en route plein ecran
#os.system("xte 'mousemove 1507 849' 'mouseclick 2'")
os.system("xte 'mousemove 1507 849' 'mouseclick 1'")
os.system("xte 'mousemove 380 580' 'mouseclick 1'")  # plein ecran de secours
os.system("xte 'sleep 3'")  # attente pour que les ecranx soient bien charges

nom_fichier=screengrab2()
txt = tool.image_to_string(
    Image.open(nom_fichier),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)


#cap souhaite
cap_s=286
cap_r=int(txt)


delta=cap_s-cap_r
for i in range (delta):
    os.system("xte 'mousemove 223 710' ")
    os.system("xte 'usleep 500000'")
    os.system("xte  'mouseclick 2'")
time.sleep(1)
    #verification
nom_fichier = screengrab2()
txt = tool.image_to_string(
    Image.open(nom_fichier),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)
time.sleep(5)
os.system("xte 'mousemove 959 538' ")
os.system("xte  'mouseclick 2'")
os.system("xte  'mouseclick 1'")
os.system("xte 'sleep 1'")
os.system("xte 'mousemove 319 843' ")
os.system("xte  'mouseclick 2'")
os.system("xte  'mouseclick 2'")
os.system("xte  'mouseclick 1'")
time.sleep(2)
nom_fichier2=screengrab3()
txt3 = tool.image_to_string(
    Image.open(nom_fichier2),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)
print(txt3)

cap=int(txt)
if cap==cap_s :
    os.system("xte 'mousemove 370 635' ")
    os.system("xte  'mouseclick 2'")
    os.system("xte  'mouseclick 1'")
    print ('les 2 caps sont identiques')