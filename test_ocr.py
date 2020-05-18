from PIL import Image
import sys
import pyscreenshot as ImageGrab
import pyocr
import pyocr.builders
import time
import os

os.system("xte 'mousermove -300 -300'")

os.system("xte 'mousemove 223 710' 'mouseclick 2'")


for i in range (5):
    os.system("xte 'usleep 500000'")
    os.system("xte 'mouseclick 2'")


tools = pyocr.get_available_tools()
# The tools are returned in the recommended order of usage
tool = tools[0]
#print (tools)


langs = tool.get_available_languages()
print (langs)
lang = langs[0]
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.


def screengrab2():
    boxt = (209, 600, 280, 638)
    imt = ImageGrab.grab(boxt)
    file_adress = '/home/jphe/PycharmProjects/Captures/total' + str(int(time.time())) + '.png'
    imt.save(file_adress, 'PNG')
    return file_adress

nom_fichier=screengrab2()
txt = tool.image_to_string(
    Image.open(nom_fichier),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)

print ('texte retourne')
print ('txt : ',txt)

# txt is a Python string
#
# word_boxes = tool.image_to_string(
#     Image.open('test.png'),
#     lang="eng",
#     builder=pyocr.builders.WordBoxBuilder()
# )