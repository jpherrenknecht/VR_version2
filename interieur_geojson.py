import folium
import webbrowser

def chaine_to_dec(latitude, longitude):
    ''' Transforme les chaines latitude et longitude en un tuple (x,y) '''
    degre = int(latitude[0:3])
    minutes = int(latitude[4:6])
    secondes = int(latitude[7:9])
    lat = degre + minutes / 60 + secondes / 3600
    if latitude[10] == 'N':
        lat = -lat
    degre = int(longitude[0:3])
    minutes = int(longitude[4:6])
    secondes = int(longitude[7:9])
    long = degre + minutes / 60 + secondes / 3600
    if longitude[10] == 'W':
        long = -long

    return (long, lat)

def chaine_to_cplx(latitude, longitude):
    ''' Transforme les chaines latitude et longitude en un complexe  (x+iy) '''
    degre = int(latitude[0:2])
    minutes = int(latitude[3:5])
    secondes = int(latitude[6:8])
    lat = degre + minutes / 60 + secondes / 3600
    if latitude[9] == 'N':
        lat = -lat
    degre = int(longitude[0:2])
    minutes = int(longitude[3:5])
    secondes = int(longitude[6:8])
    long = degre + minutes / 60 + secondes / 3600
    if longitude[9] == 'W':
        long = -long
    position = long + lat * 1j

    return position


def cplx(d):
    ''' transforme un tuple en nparray complex'''
    D = (d[0] + d[1] * 1j)
    return D

#todo ###############################################################"
# Depart ###########################################################"
latitude_d = '017-30-58-N'
longitude_d = '056-38-32-W'
#todo
# Arrivee
latitude_a = '017-53-00-N'
longitude_a = '062-49-00-W'

d = chaine_to_dec(latitude_d, longitude_d)  # conversion des latitudes et longitudes en tuple
ar = chaine_to_dec(latitude_a, longitude_a)

D = cplx(d)  # transformation des tuples des points en complexes
A = cplx(ar)

lat1=-(d[1]+ar[1])/2                    # Point pour centrer la carte folium
long1= (d[0]+ ar[0])/2
print('Depart : Latitude {:6.4f}  Longitude {:6.4f}'.format(d[1], d[0]))
print('Arrivee: Latitude {:4.2f}  Longitude {:4.2f}'.format(ar[1], ar[0]))





if __name__ == '__main__':
    lat1=-24
    long1=24
    m = folium.Map(location=[lat1, long1], zoom_start=5)

    geojs=    {  "type": "FeatureCollection", "features": [
            {               "type": "Feature",               "properties": {},
                "geometry": {                    "type": "Polygon",
                    "coordinates": [                        [
                            [                             11.074218749999998,                                -16.97274101999901
                            ],                            [                                19.335937499999996,
                                -34.74161249883172                            ],
                            [                                28.30078125,                                -33.7243396617476
                            ],                            [                                35.33203125,
                                -19.808054128088575                            ],
                            [                                11.074218749999998,                                -16.97274101999901
                            ]            ]             ]           }     }     ]   }

    point=[-25.48,24.43]
    folium.GeoJson(geojs).add_to(m)
    folium.Circle(point, color='black', radius=200, tooltip='test tooltip', popup='test popup',fill=True).add_to(m)

    folium.LatLngPopup().add_to(m)

    # folium.GeoJson(
    #     antarctic_ice_edge,
    #     name='geojson'
    # ).add_to(m)

    # Initialisation carte folium **************************************************************

    #*******************************************************************************************
    filepath = '~\map.html'
    m.save(filepath)
    webbrowser.open( filepath)