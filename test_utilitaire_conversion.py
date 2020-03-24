latitude = '46-44-60-N'
longitude = '03-12-28-W'

def chaine_to_dec(latitude,longitude):
    ''' Convertit deux chaines latitude longitude en tuple (x,y)'''
    degre = int(latitude[0:2])
    minutes = int(latitude[3:5])
    secondes = int(latitude[6:8])
    lat=degre+minutes/60+secondes/3600
    if latitude[9]=='N':
        lat=-lat
    degre = int(longitude[0:2])
    minutes = int(longitude[3:5])
    secondes = int(longitude[6:8])
    long = degre + minutes / 60 + secondes / 3600
    if longitude[9]=='W':
        long=-long

    return (lat,long)


# depart

latitude = '46-44-60-N'
longitude = '03-12-28-W'
#
# degre=int(latitude[0:2])
# minutes=int(latitude[3:5])
# secondes=int(latitude[6:8])
# print(latitude[9])
#
# print (degre)
# print(minutes)
# print(secondes)
#
# decimal=degre+minutes/60+secondes/3600
#
# print (decimal)

valeur=chaine_to_dec(latitude,longitude)
print(valeur)