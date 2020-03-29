from urllib.request import urlretrieve
import cfgrib
import xarray as xr
import time
import pandas as pd
import math
import numpy as np
import datetime
import h5py
import os


def interpol2(tableau, y, x):
    # LES INDICES VARIENT DE 1 EN 1,  tableau donne les valeurs tableau[y,x]
    x1 = math.floor(x - 1E-5)  # x2=x1+1   , x2-x1=1
    y1 = math.floor(y - 1E-5)  # y2=y1+1   , y2-y1= 1
    dx = x - x1
    dy = y - y1

    #print('intermediaire', y1, x1)
    delta_fx = tableau[y1, x1 + 1] - tableau[y1, x1]
    delta_fy = tableau[y1 + 1, x1] - tableau[y1, x1]
    delta_fx_fy = tableau[y1, x1] + tableau[y1 + 1, x1 + 1] - tableau[y1, x1 + 1] - tableau[y1 + 1, x1]
    f_x_y = delta_fx * dx / 1 + delta_fy * dy / 1 + delta_fx_fy * dx * dy / (1 * 1) + tableau[y1, x1]
    return f_x_y


def interpol3(tab2, z, y, x):
    dimz, dimy, dimx = tab2.shape
    if (z > dimz - 1) or (y > dimy - 1) or (x > dimx - 1):
        print('Erreur de dimension dans les donnees de l interpolation')
    z1 = math.floor(z - 1E-5)

    #print('resultat intermediaire ', z1, y, x)
    xy1 = interpol2(tab2[z1, :, :], y, x)
    xy2 = interpol2(tab2[z1 + 1, :, :], y, x)
    resultat = (z - z1) / 1 * (xy2 - xy1) + xy1
    return resultat

def chainetemps_to_int(chainetemps):
    '''Convertit une chaine de temps en valeur entiere '''
    '''retourne egalement le temps en s ou le temps formate '''
    day = int(chainetemps[0:2])
    month = int(chainetemps[3:5])
    year = int(chainetemps[6:10])
    hour = int(chainetemps[11:13])
    mins = int(chainetemps[14:16])
    secs = int(chainetemps[17:19])
    strhour=chainetemps[11:13]
    date = chainetemps[6:10] + chainetemps[3:5] + chainetemps[0:2]
    tig = time.mktime((year, month, day, hour, mins, secs, 0, 0, 0))
    formate=time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(tig))
    return tig,day,month,year,hour,mins,secs,date,strhour,formate


def chargement_grib(dategrib):

    '''Charge le grib a la date indiquée et le sauve en type tableau de complexes sous format hd5'''
    tig, day, month, year, hour, mins, secs, date ,strhour,formate=chainetemps_to_int(dategrib)
    leftlon,rightlon,toplat,bottomlat  = 0,360,90,-90
    iprev = ()
    for a in range(0, 387, 3):                           #Construit le tuple des indexs des fichiers maxi 387
        iprev += (str(int(a / 100)) + str(int((a % 100) / 10)) + str(a % 10),)
    GR = np.zeros((len(iprev), 181, 360),dtype=complex) #initialise le np array de complexes qui recoit les donnees
    for indexprev in range(len(iprev)):                 # recuperation des fichiers
        prev = iprev[indexprev]
        print (' Enregistrement prévision {} + {} heures : '.format(dategrib,prev))                    # destine a suivre le chargement des previsions
        url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl?file=gfs.t" + strhour + "z.pgrb2.1p00.f" + \
              prev + "&lev_10_m_above_ground=on&all_var=on&leftlon=" \
              + str(leftlon) + "&rightlon=" + str(rightlon) + "&toplat=" + str(toplat) + "&bottomlat=" + str(
              bottomlat) + "&dir=%2Fgfs." + date + "%2F" + strhour
        nom_fichier = "grib_" + date + "_" + strhour + "_" + prev
        urlretrieve(url, nom_fichier)  # recuperation des fichiers

        #exploitation du fichier et mise en memoire dans GR
        ds = xr.open_dataset(nom_fichier, engine='cfgrib')
        GR[indexprev]=ds.variables['u10'].data+ds.variables['v10'].data*1j
        os.remove(nom_fichier)  # On efface le fichier pour ne pas encombrer
        os.remove(nom_fichier+'.4cc40.idx')
    #sauvegarde dans fichier du tableau GR
    filename = "gribs/grib_gfs_" + dategrib + ".hdf5"
    f1 = h5py.File(filename, "w")
    dset1 = f1.create_dataset("dataset_01", GR.shape, dtype='complex', data=GR)
    dset1.attrs['time_grib'] = tig
    f1.close()

    return  filename


def ouverture_fichier(filename):
    # ouverture du fichier
    f2 = h5py.File(filename, 'r')
    list(f2.keys())
    dset1 = f2['dataset_01']
    GR = dset1[:]
    tig = dset1.attrs['time_grib']

    V=np.abs(GR)*1.94384
    U=(270-np.angle(GR,deg=True))%360
    return tig,U,V



def prevision(tig,A,V,tp,latitude,longitude):
    itemp =(tp - tig) / 3600 / 3
    ilati = (latitude + 90)
    ilong = ( longitude)%360
    #print ('indices',itemp,ilati,ilong)
    vit_vent_n =interpol3(V,itemp,ilati,ilong)
    angle_vent =interpol3(A,itemp,ilati,ilong)

    return vit_vent_n, angle_vent



if __name__ == '__main__':

    heures=['00','06','12','18']
    t=time.localtime()
    utc=time.gmtime()
    decalage=t[3]-utc[3]

    heure_grib=heures[ ((utc[3]+13)//6)%4 ]

    dategrib=str(t[2]//10)+str(t[2]%10)+'-'+str(t[1]//10) + str(t[1]%10)+'-'+str(t[0])+'T'+heure_grib+'-00-00'
    filenamehd5 = "gribs/grib_gfs_" + dategrib + ".hdf5"
    print ('nom fichier',filenamehd5)
    if os.path.exists(filenamehd5)==False :
        filenamehd5 = chargement_grib(dategrib)


# Données pour prevision en UTC
    dateprev=('25-03-2020T22-00-00')
    #dateprev=time.strftime("%d-%m-%YT%H-%M-%S", time.gmtime(time.time()))
    latitude  = -48  # Psitif si sud
    longitude = -13.5  # Positif si est

    tp=chainetemps_to_int(dateprev)[0]                  # calcul du moment de la prevision en s
    tp_formate=chainetemps_to_int(dateprev)[9]          # utilisation pour impressions
    tig,U,V=ouverture_fichier(filenamehd5)              # ouverture du fichier hd5
    vit_vent_n, angle_vent=prevision(tig,U,V,tp,latitude,longitude) # Calcul de la prevision

    # Impression des resultats
    print('\nDate et Heure du grib :', time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(tig)))
    print('Heure de la prevision :', tp_formate)

    print('\nLe {} Pour latitude {:6.2f} et longitude{:6.2f} '.format(tp_formate, latitude, longitude))
    print('    Vitesse du vent {:6.3f} Noeuds'.format(vit_vent_n))
    print('    Angle du vent   {:6.1f} °'.format(angle_vent))





#Fichier commite en master
dateprev = ('07-03-2020T17-40-00')


instant=time.time()
print (' time en s ',instant)

formate=time.strftime(" %d %b %Y %H:%M:%S ", time.gmtime(instant))
format2=time.strftime("%d-%m-%YT%H-%M-%S", time.gmtime(time.time()))


print('temps formate',formate)

print('instant UTC formate',format2)

#

tij = time.mktime((2020, 3, 24, 00, 00, 00, 0, 0, 0))

print ('debut journee',tij)

print (datetime.date.today())
#: permet de récupérer l'année, le mois (entre 1 et 12), le jour, l'heure, la minute et la seconde.
#mise a jour automatique du grib








# #Utilisation avec lecture du fichier h5py
# date = dategrib[6:10] +dategrib[3:5] +dategrib[0:2]
# filename = "gribs/grib_gfs_" + date + ".hdf5"
#
# f2 = h5py.File(filename, 'r')
# list(f2.keys())
#
# dset1 = f2['dataset_01']
# data1 = dset1[:]
# time2=dset1.attrs['time_grib']




    # pour le gfs 06
    # Debut des modifications a 9h30 UTC - 12h de donnees toutes les 10 mn
    #                         a 10h 30    1 semaine de donnees sont a jour
    #                         a 11 h      toutes les previsions sont connues
    # Le jeu semble interpoler les donnees entre l ancien et le nouveau modele meteo pendant 1 h
    # Zezo commence a changer les données 1 h après soit a partir de 10h 30 UTC
    # Pour calculer une route longue il vaut mieux attendre la fin des mises a jour soit 11 h UTC soit 12 h heure d hiver , pour une route courte on peut regarder les changement a partir de 10h 30 UTC soit 11 h30
    #
    # sur ZEZO La ligne rouge indique la position previsionelle  à partir de laquelle les nouveaux gribs sont pris en compte
