#!/bin/env python3
# coding: utf-8
import os
import time
import math
import numpy as np
from urllib.request import urlretrieve
import xarray as xr
import h5py
from scipy.interpolate import RegularGridInterpolator
from pathlib import Path

# les gribs complets sont disponibles en heure d'ete à
# 13h(gfs06) - 19(gfs12) -  01(gfs18) - 07 h (gfs00)
# les gribs complets sont disponibles en heure d'hiver à
# 12h(gfs06) - 18(gfs12) -  00(gfs18) - 06 h (gfs00)

# renvoie le chemin absolu du repertoire courant ici /home/jphe/PycharmProjects/VR_version2
basedir = os.path.abspath(os.path.dirname(__file__))



ix = np.arange(129)  # temps
iy = np.arange(181)  # latitudes
iz = np.arange(360)  # longitudes


def chainetemps_to_int(chainetemps):
    '''Convertit une chaine de temps en valeur entiere '''
    '''retourne egalement le temps en s ou le temps formate '''
    day = int(chainetemps[0:2])
    month = int(chainetemps[3:5])
    year = int(chainetemps[6:10])
    hour = int(chainetemps[11:13])
    mins = int(chainetemps[14:16])
    secs = int(chainetemps[17:19])
    strhour = chainetemps[11:13]
    date = chainetemps[6:10] + chainetemps[3:5] + chainetemps[0:2]

    t = time.localtime()
    utc = time.gmtime()
    decalage_s = (t[3] - utc[3]) * 3600
    t_s_local = time.mktime((year, month, day, hour +1, mins, secs, 0, 0, 0))
    t_s_utc = t_s_local - decalage_s
    #todo pourquoi le +1
    formate_local = time.strftime(" %d %b %Y %H:%M:%S ", time.gmtime(t_s_local))
    # t_s est un temps en secondes locales
    return t_s_local, day, month, year, hour, mins, secs, date, strhour, formate_local, t_s_utc


def chaine_to_dec_old(latitude, longitude):
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

def chargement_grib():
    '''Charge le grib a la date indiquée et le sauve en type tableau de complexes sous format hd5'''



    heures = ['00', '06', '12', '18']
    t = time.localtime()
    utc = time.gmtime()
    decalage_h = t[3] - utc[3]
    decalage_s = decalage_h * 3600



    #on bloque l(heure du grib
    heure_grib = heures[((utc[3] + 19) // 6) % 4]  #
    #si utc inferieur à 5 la date doit etre celle de la veille

    if utc[3]<5:
        utc = time.gmtime(time.time() -18000)


    dategrib = str(utc[2] // 10) + str(utc[2] % 10) + '-' + str(utc[1] // 10) + str(utc[1] % 10) + '-' + str(
        utc[0]) + ' ' + heure_grib + '-00-00'

    #print ('dategrib',dategrib)

    filename="gribs/grib_gfs_" + dategrib + ".hdf5"
    filenamehdf5 = os.path.join(basedir,filename)
   # filenamehd5 = "~/PycharmProjects/VR_version2/gribs/grib_gfs_" + dategrib + ".hdf5"
    print('Emplacement fichier hdf5 : ', filenamehdf5)
    # print('heure grib utc ', int(heure_grib))

    if os.path.exists(filenamehdf5) == False:
        tlocal, day, month, year, hour, mins, secs, date, strhour, formate, t_s_utc = chainetemps_to_int(dategrib)

        print('valeur de tlocal', tlocal)
        # print('tig au debut chargement grib',tig)
        print('tlocal au debut chargement grib', tlocal)

        leftlon, rightlon, toplat, bottomlat = 0, 360, 90, -90
        iprev = ()
        for a in range(0, 387, 3):  # Construit le tuple des indexs des fichiers maxi 387
            iprev += (str(int(a / 100)) + str(int((a % 100) / 10)) + str(a % 10),)
        GR = np.zeros((len(iprev), 181, 360),
                      dtype=complex)  # initialise le np array de complexes qui recoit les donnees

        for indexprev in range(len(iprev)):  # recuperation des fichiers
            prev = iprev[indexprev]

            url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl?file=gfs.t" + strhour + "z.pgrb2.1p00.f" + \
                  prev + "&lev_10_m_above_ground=on&all_var=on&leftlon=" \
                  + str(leftlon) + "&rightlon=" + str(rightlon) + "&toplat=" + str(toplat) + "&bottomlat=" + str(
                bottomlat) + "&dir=%2Fgfs." + date + "%2F" + strhour
            nom_fichier = "grib_" + date + "_" + strhour + "_" + prev

            urlretrieve(url, nom_fichier)  # recuperation des fichiers

            print(' Enregistrement prévision {} + {} heures effectué: '.format(dategrib,
                                                                               prev))  # destine a suivre le chargement des previsions

            # exploitation du fichier et mise en memoire dans GR
            ds = xr.open_dataset(nom_fichier, engine='cfgrib')

            GR[indexprev] = ds.variables['u10'].data + ds.variables['v10'].data * 1j

            os.remove(nom_fichier)  # On efface le fichier pour ne pas encombrer
            os.remove(nom_fichier + '.4cc40.idx')

        # sauvegarde dans fichier hdf5 du tableau GR
        #filename = "~/PycharmProjects/VR_version2/gribs/grib_gfs_" + dategrib + ".hdf5"
        f1 = h5py.File(filenamehdf5, "w")
        dset1 = f1.create_dataset("dataset_01", GR.shape, dtype='complex', data=GR)

        dset1.attrs['time_grib'] = tlocal  # transmet le temps local en s pour pouvoir faire les comparaisons
        f1.close()

    return filenamehdf5


def ouverture_fichier(filename):
    # ouverture du fichier
    f2 = h5py.File(filename, 'r')
    list(f2.keys())
    dset1 = f2['dataset_01']
    GR = dset1[:]
    tig = dset1.attrs['time_grib']
    f2.close()
    return tig, GR


def prevision(tig, GR, tp, latitude, longitude):
    fn3 = RegularGridInterpolator((ix, iy, iz), GR)
    itemp = (tp - tig) / 3600 / 3
    ilati = (latitude + 90)
    ilong = (longitude) % 360

    #print ('indices',itemp,ilati,ilong )

    vcplx = fn3((itemp, ilati, ilong))
    #print('vcplx',vcplx)
    vit_vent_n = np.abs(vcplx) * 1.94384
    angle_vent = (270 - np.angle(vcplx, deg=True)) % 360
    return vit_vent_n, angle_vent

def prevision_tableau (tig,GR,tp,points):
    '''Le tableau des points est un tableau de points complexes'''
    '''retourne un tableau des previsions angles et vitesses '''
    fn3 = RegularGridInterpolator((ix, iy, iz), GR)
    itemp=np.ones( points.shape)*(tp - tig) / 3600 / 3
    ilati = np.imag(points) + 90
    ilong = np.real(points) %360
    e=np.concatenate((itemp.T,ilati.T,ilong.T ),axis=1)

    # print ('e.shape)',e.shape)
    # print ('e',e)
    prevs = fn3((e))   #prevs est un tableau de complexes des vecteurs du vent aux differents points
    vitesse = np.abs(prevs) * 1.94384
    #print (vitesse)
    angle_vent = (270 - np.angle(prevs, deg=True)) % 360
    #print (angle_vent)

    return vitesse, angle_vent


def prevision_tableau2 (GR,temp,point):
    ''' calcule les previsions a partir d'une liste des temps par rapport au depart et des points sous forme complexe'''
    temps = temp.reshape((1, -1))
    points=point.reshape((1, -1))
    fn3 = RegularGridInterpolator((ix, iy, iz), GR)
    tab_itemp=temps.reshape((1,-1))/ 3600 / 3
    ilati = np.imag(points) + 90
    ilong = np.real(points) %360
    e = np.concatenate(( tab_itemp.T, ilati.T, ilong.T), axis=1)
    prevs = fn3((e))   #prevs est un tableau de complexes des vecteurs du vent aux differents points
    vitesse = np.abs(prevs) * 1.94384
    #print (vitesse)
    angle_vent = (270 - np.angle(prevs, deg=True)) % 360
    #print (angle_vent)

    return vitesse, angle_vent

if __name__ == '__main__':
    filename = chargement_grib()
    tig, GR = ouverture_fichier(filename)
    # Depart
    latitude_d = '021-44-19-N'
    longitude_d = '160-23-01-W'
    # # Depart
    # latitude_d = '39-00-00-N'
    # longitude_d = '67-00-00-W'
    # Arrivee
    latitude_a = '12-10-00-N'
    longitude_a = '65-00-00-W'


    dateprev = ('04-04-2020 12-21-00')  # a indiquer en local

    dateprev_s = chainetemps_to_int(dateprev)[10]
    dateprev_formate = chainetemps_to_int(dateprev)[9]

    d = chaine_to_dec(latitude_d, longitude_d)  # co
    print ('d :',d)


# version avec temps instantane


    t = time.localtime()
    instant = time.time()+3600

    print ('t1',t[3])

    instant_formate = time.strftime(" %d %b %Y %H:%M:%S  ", time.gmtime(instant))

    print('tig', tig)
    print ('instant en secondes' ,instant)
    print('dateprev en s ', dateprev_s)
    print('instant formate', instant_formate)

    print('\n VERSION AVEC INSTANT------------------------------------- ')

    vit_vent_n, angle_vent = prevision(tig, GR, instant, d[1], d[0])
    print('\nLe {} heure UTC Pour latitude {:6.2f} et longitude{:6.2f} '.format(instant_formate, d[1], d[0]))
    print('\tAngle du vent   {:6.1f} °'.format(angle_vent))
    print('\tVitesse du vent {:6.3f} Noeuds'.format(vit_vent_n))




    # version tableau ******************************************************************************

    #points=np.array([[-67-39*1j, -65-40*1j]])
    #points = np.array([[d[0] + d[1] * 1j]])
    points = np.array([[-10 - 2 * 1j, -15 + 3 * 1j, 50 + 10 * 1j]])


    prevs=prevision_tableau(tig, GR, instant, points)
    print(prevs)

    # print ('\nVERSION AVEC DATE EN DUR------------------------------------ ')
    #
    # for k in range (0,5,1):
    #     dateprev_s+=3600
    #     date_prev_formate = time.strftime(" %d %b %Y %H:%M:%S ", time.gmtime(dateprev_s))
    #     vit_vent_n, angle_vent = prevision(tig, GR, dateprev_s, d[1], d[0])
    #     print('\nLe {} heure UTC Pour latitude {:6.2f} et longitude{:6.2f} '.format(date_prev_formate, d[1], d[0]))
    #     print('\tAngle du vent   {:6.1f} °'.format(angle_vent))
    #     print('\tVitesse du vent {:6.3f} Noeuds'.format(vit_vent_n))
    #
    #     print()
