import folium
import shapely
#import geopandas as gpd
from shapely.geometry import Point,Polygon
from shapely import speedups
import pickle
import webbrowser

point1=Point(30.30,-30.45) # point terre longitude en premier
point2=Point(31.54,-29.48) # point mer



with open("afrique.txt", "rb") as fp:
#with open("listes.txt", "rb") as fp:
    contour = pickle.load(fp)

# creation objet shapely
a=Polygon(contour)
cont_xy=[]
for i in range (len(contour)):
    cont_xy.append([contour[i][1],contour[i][0]])

if point1.within(a):
    print ("le point 1 est à terre" )
else:
    print ("le point 1 est en mer" )


if point2.within(a):
    print ("le point 2 est à terre" )
else:
    print ("le point 2 est en mer" )

monde = folium.Map(location = [48.856578, 2.351828], zoom_start = 3)
folium.LatLngPopup().add_to(monde)   # popup permettant d'afficher latitude et longitude
folium.PolyLine(cont_xy,color='blue', popup='ligne de cotes').add_to(monde)

folium.Marker([point1.y,point1.x],icon=folium.Icon(color='red', icon='info-sign'), popup = "Test_a_terre").add_to(monde)
folium.Marker([point2.y,point2.x],icon=folium.Icon(color='blue'), popup = "Test_en mer").add_to(monde)

#monde

filepath = '~\monde.html'
monde.save(filepath)
webbrowser.open( filepath)