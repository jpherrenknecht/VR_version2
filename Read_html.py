import urllib
import urllib.request

url='https://www.virtualregatta.com/fr/offshore-jeu/'
#sock = urllib.urlopen(url)
with urllib.request.urlopen(url) as response:
   html = response.read()
print (html)

#
# htmlSource = sock.read()
# sock.close()
# print (htmlSource)