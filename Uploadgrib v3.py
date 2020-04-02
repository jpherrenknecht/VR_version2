from urllib.request import urlretrieve
import xarray as xr
import time
import math
import numpy as np
import h5py
import os

# les gribs complets sont disponibles en heure d'ete à
# 13h(gfs06) - 19(gfs12) -  01(gfs18) - 07 h (gfs00)


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

    t = time.localtime()
    utc = time.gmtime()
    decalage_s = (t[3] - utc[3]) * 3600
    t_s_local = time.mktime((year, month, day, hour+1, mins, secs, 0, 0, 0))
    #todo pourquoi le +1
    t_s_utc =t_s_local-decalage_s

    formate_local=time.strftime(" %d %b %Y %H:%M:%S ", time.gmtime(t_s_local))
    #t_s est un temps en secondes locales
    return t_s_local,day,month,year,hour,mins,secs,date,strhour,formate_local,t_s_utc

def chaine_to_dec(latitude, longitude):
    ''' Transforme les chaines latitude et longitude en un tuple (x,y) '''
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

    return (long, lat)


def chargement_grib():

    '''Charge le grib a la date indiquée et le sauve en type tableau de complexes sous format hd5'''

    heures = ['00', '06', '12', '18']
    t = time.localtime()
    utc = time.gmtime()
    decalage_h = t[3] - utc[3]
    decalage_s = decalage_h * 3600
    # print ('Decalage',decalage_h )

    heure_grib = heures[((utc[3] + 19) // 6) % 4]  #
    dategrib = str(t[2] // 10) + str(t[2] % 10) + '-' + str(t[1] // 10) + str(t[1] % 10) + '-' + str(
        t[0]) + ' ' + heure_grib + '-00-00'
    filenamehd5 = "gribs/grib_gfs_" + dategrib + ".hdf5"
    print('Nom fichier hdf5 : ', filenamehd5)
    #print('heure grib utc ', int(heure_grib))

    if os.path.exists(filenamehd5) == False:
        tlocal, day, month, year, hour, mins, secs, date ,strhour,formate,t_s_utc=chainetemps_to_int(dategrib)

        print ('valeur de tlocal',tlocal)
        # print('tig au debut chargement grib',tig)
        print('tlocal au debut chargement grib', tlocal)

        leftlon,rightlon,toplat,bottomlat  = 0,360,90,-90
        iprev = ()
        for a in range(0, 387, 3):                           #Construit le tuple des indexs des fichiers maxi 387
            iprev += (str(int(a / 100)) + str(int((a % 100) / 10)) + str(a % 10),)
        GR = np.zeros((len(iprev), 181, 360),dtype=complex) #initialise le np array de complexes qui recoit les donnees

        for indexprev in range(len(iprev)):                 # recuperation des fichiers
            prev = iprev[indexprev]

            url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl?file=gfs.t" + strhour + "z.pgrb2.1p00.f" + \
                  prev + "&lev_10_m_above_ground=on&all_var=on&leftlon=" \
                  + str(leftlon) + "&rightlon=" + str(rightlon) + "&toplat=" + str(toplat) + "&bottomlat=" + str(
                  bottomlat) + "&dir=%2Fgfs." + date + "%2F" + strhour
            nom_fichier = "grib_" + date + "_" + strhour + "_" + prev
            urlretrieve(url, nom_fichier)  # recuperation des fichiers

            print (' Enregistrement prévision {} + {} heures effectué: '.format(dategrib,prev))                    # destine a suivre le chargement des previsions

            #exploitation du fichier et mise en memoire dans GR
            ds = xr.open_dataset(nom_fichier, engine='cfgrib')

            GR[indexprev]=ds.variables['u10'].data+ds.variables['v10'].data*1j

            os.remove(nom_fichier)  # On efface le fichier pour ne pas encombrer
            os.remove(nom_fichier+'.4cc40.idx')

        #sauvegarde dans fichier du tableau GR
        filename = "gribs/grib_gfs_" + dategrib + ".hdf5"
        f1 = h5py.File(filename, "w")
        dset1 = f1.create_dataset("dataset_01", GR.shape, dtype='complex', data=GR)

        dset1.attrs['time_grib'] = tlocal   # transmet le temps local en s pour pouvoir faire les comparaisons
        f1.close()

    return  filenamehd5


def ouverture_fichier(filename):
    # ouverture du fichier
    f2 = h5py.File(filename, 'r')
    list(f2.keys())
    dset1 = f2['dataset_01']
    GR = dset1[:]
    tig = dset1.attrs['time_grib']
    V=np.abs(GR)*1.94384
    #todo ajoute 360 pour pb interpolation entre 359 et 1 sans effet
    U=(270-np.angle(GR,deg=True))%360
    # voir a fermer le fichier

    return tig,U,V


def prevision(tig,X,Y,tp,latitude,longitude):
    itemp =int((tp - tig) / 3600/3)
    ilati =int( (latitude + 90))
    ilong = int(( longitude)%360)
    print ('indices',itemp,ilati,ilong)
    vit_vent_n =Y[itemp][ilati][ilong]
    angle_vent =X[itemp][ilati][ilong]
    return vit_vent_n, angle_vent




if __name__ == '__main__':
    filename=chargement_grib()
    tig,X,Y=ouverture_fichier(filename)

    latitude_d = '39-00-00-N'
    longitude_d = '64-00-00-W'
    dateprev = ('01-04-2020 17-00-00')  # a indiquer en local

    dateprev_s = chainetemps_to_int(dateprev)[10]
    dateprev_formate = chainetemps_to_int(dateprev)[9]
    d = chaine_to_dec(latitude_d, longitude_d)  # co


# on essaie avec des valeurs entieres
    vit_vent_n, angle_vent=prevision(tig,X,Y,dateprev_s,d[1],d[0])
    print('\nLe {} heure locale Pour latitude {:6.2f} et longitude{:6.2f} '.format(dateprev_formate, d[1], d[0]))
    print('\tVitesse du vent {:6.3f} Noeuds'.format(vit_vent_n))
    print('\tAngle du vent   {:6.1f} °'.format(angle_vent))
    print()
