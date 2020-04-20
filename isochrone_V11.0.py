#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 08:52:41 2019
# les gribs complets sont disponibles en heure d'ete à
# 13h(gfs06) - 19(gfs12) -  01(gfs18) - 07 h (gfs00)

@author: jph
"""
# test
import os
import time
import math
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
from Uploadgrib import *
#from polaires_caravelle import *
from polaires_figaro2 import *
from operator import itemgetter



# *****************************************   Donnees   ****************************************************************


# dans tous les calculs la longitude correspondant à l'axe des x est prise en premier
# Les points sont definis en longitude (x) latitude (y)
# Attention les previsions sont elles faites en latitude longitude
# les latitudes sont positives vers le sud et les longitudes positives vers l'est
# Les points initiaux sont sous forme de tuple longitude latitude
# les angles sont des angles trigo
# pour le vent on parle de vitesses et angles




# **************************************   Fonctions   ******************************************************************

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
    position=long+lat*1j

    return position






def cplx(d):
    ''' transforme un tuple en nparray complex'''
    D = (d[0] + d[1]* 1j)
    return D


def rangecap(direction_objectif, d_vent, angle_objectif, angle_twa_pres, angle_twa_ar):
    '''retourne le range des caps possibles '''
    '''on vise l'objectif sous un angle maxi de 2fois l angle objectif'''
    '''on exclut les twa trop au près ou trop au vent arriere'''
    d_vent, d_objectif = int(d_vent), int(angle_objectif)
    a = (d_objectif - angle_objectif)
    b = (d_objectif + angle_objectif) + 1
    c = (d_vent - angle_twa_pres)
    d = (d_vent + angle_twa_pres) + 1
    e = d_vent + 180 + angle_twa_ar + 1
    f = d_vent + 180 - angle_twa_ar
    rangecap = np.intersect1d(np.intersect1d((np.arange(a, b, 1)) % 360, (np.arange(d, c + 360)) % 360),
                              (np.arange(e, f + 360)) % 360)
    return rangecap


def calcul_points(D, tp, d_t, angle_vent, vit_vent, range, polaires):
    '''tp temps au point D; d_t duree du deplacement en s ; angle du vent au point ; Vitesse du vent au point ; caps a simuler  ; polaires du bateau  '''
    '''retourne un tableau points sous forme de valeurs complexes'''
    points_arrivee = np.zeros((range.shape),   dtype=complex)  # Init tableau   points d'arrivee sous forme complexe
    range_radian = (-range + 90) * math.pi / 180
    vit_noeuds = polaire2_vect(polaires, vit_vent, angle_vent, range)  # Vitesses suivant les differents caps

    # print ('vit_noeuds',vit_noeuds)
    # print ('vit_noeuds',vit_noeuds.shape)
    # print( 'range_radian shape',range_radian.shape)
    # print('D.shape',D.shape)
    points_arrivee = D + (d_t / 3600 / 60 * vit_noeuds * (np.sin(range_radian) / math.cos(D.imag * math.pi / 180) - np.cos(range_radian) * 1j))
    return points_arrivee, tp + d_t


def deplacement(D, A):
    '''retourne la distance et l'angle du deplacement entre le depart et l'arrivee'''
    C = A - D
    return np.abs(C), (90 - np.angle(C, deg=True))

def deplacement2(D, A):
    '''retourne la distance et l'angle du deplacement entre le depart et l'arrivee'''
    C = A - D
    return np.abs(C), (450 + np.angle(C, deg=True))%360





def rangenavi(capa, capb):
    if capb > capa:
        range = np.arange(capa, capb)
    else:
        range = np.concatenate((np.arange(0, capb + 1), np.arange(capa, 360)), axis=0)
    return range


def range_cap(direction_objectif, direction_vent, a_vue_objectif, angle_pres, angle_var):

    # print ('direction_vent indice i',direction_vent)
    # print('direction_objectif indice i', direction_objectif)
    direction_vent, direction_objectif = int(direction_vent), int(direction_objectif)
    cap1 = (direction_vent + angle_pres) % 360
    cap2 = (direction_vent - angle_pres + 1) % 360
    cap3 = (180 + direction_vent + angle_var) % 360
    cap4 = (180 + direction_vent - angle_var + 1) % 360
    cap5 = (direction_objectif - a_vue_objectif) % 360
    cap6 = (direction_objectif + a_vue_objectif) % 360

    z1 = rangenavi(cap1, cap4)
    z2 = rangenavi(cap3, cap2)
    z3 = rangenavi(cap5, cap6)
    range1 = np.intersect1d(z1, z3)
    range2 = np.intersect1d(z2, z3)

    rangetotal = np.concatenate((range1, range2), axis=0)
    return rangetotal

def f_isochrone(pt_init_cplx, temps_initial_iso):
    ''' Calcule le nouvel isochrone a partir d'un tableau de points pt2cplx tableau numpy de cplx'''
    ''' deltatemps, tig , U, V sont supposees etre des variables globales'''
    ''' Retourne les nouveaux points el le nouveau temps et implemente le tableau general des isochrones'''

    global isochrone,intervalles
    numero_iso = int(isochrone[-1][2] + 1)
    delta_temps = intervalles[numero_iso]  # Ecart de temps entre anciens points et nouveaux en s
    t_iso_formate = time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(temps_initial_iso + delta_temps))
    but = False
    points_calcul = []
    caps_x = []
    tab_t = []  # tableau des temps vers l arrivee en ligne directe
    print(' Isochrone N° {}  {}'.format(numero_iso, t_iso_formate))
    numero_dernier_point = (isochrone[-1][4])  # dernier point isochrone precedent
    numero_premier_point = isochrone[-1][4] - pt_init_cplx.size

    # on recupere toutes les previsions meteo d'un coup pour l'ensemble des points de depart
    vit_vent, angle_vent=prevision_tableau(tig, GR, temps_initial_iso,pt_init_cplx)

    # pour chaque point de l'isochrone precedent  donnés en entrée (isochrone précédent)
    for i in range(pt_init_cplx.size):

        #print('deplacement(pt_init_cplx[i], A)[1]',deplacement(pt_init_cplx[0][i], A)[1])
        range_caps = range_cap(    deplacement(pt_init_cplx[0][i], A)[1]    , angle_vent[i], angle_objectif, angle_twa_pres,
                           angle_twa_ar)  # Calcul des caps a etudier

        n_pts_x, nouveau_temps = calcul_points(pt_init_cplx[0][i], temps_initial_iso, delta_temps, angle_vent[i],
                vit_vent[i],range_caps, polaires)  # Calcul de la nouvelle serie generale de points sous forme de complexe

        # la tous les nouveaux points sont calcules maintenant on expurge et on stocke
        for j in range(len(n_pts_x)):
            cap_arrivee = deplacement(n_pts_x[j], A)[1]
            distance_arrivee = deplacement(n_pts_x[j], A)[0]
            points_calcul.append(
                [n_pts_x[j].real, n_pts_x[j].imag, numero_iso, numero_premier_point + i + 1, 1, distance_arrivee,
                 cap_arrivee])

            caps_x.append(cap_arrivee)

    coeff2 = 50 / (max(caps_x) - min(caps_x))  # coefficient pour ecremer et garder 50 points

    for j in range(len(points_calcul)):  # partie ecremage
        points_calcul[j][6] = int(coeff2 * points_calcul[j][6])

    pointsx = sorted(points_calcul, key=itemgetter(6, 5))  # tri de la liste de points suivant la direction (indice  " \
    pointsx = np.asarray(pointsx)
    for i in range(len(pointsx) - 1, 0, -1):  # ecremage
        if (pointsx[i][6]) == (pointsx[i - 1][6]):
            pointsx = np.delete(pointsx, i, 0)

    for i in range(len(pointsx)):  # renumerotation
        pointsx[i][4] = i + numero_dernier_point + 1
        pointsx[i][6] = int(pointsx[i][6] / coeff2)  # on retablit le cap en valeur
        dico[pointsx[i][4]] = pointsx[i][3]





        # on cherche les temps vers l'arrivee des nouveaux points
        vit_vent, angle_vent = prevision(tig, GR, nouveau_temps, pointsx[i][1], pointsx[i][0])
        twa = 180 - abs(((360 - angle_vent + pointsx[i][6]) % 360) - 180)

        resultat = polaire(polaires, vit_vent, twa)
        d_a = pointsx[i][5]
        t_a = 60 * d_a / (resultat+0.00000001)
        tab_t.append(t_a)
        # print('temps',t_a)
        if t_a < delta_temps / 3600:
            but = True
                    # indice du temps minimum

    indice = tab_t.index(min(tab_t)) + numero_dernier_point + 1
    #print ('min tabt',min(tab_t))
    isochrone = np.concatenate((isochrone, pointsx))  # On rajoute ces points a la fin du tableau isochrone
    ptn_cplx =np.array ([pointsx[:, 0] + pointsx[:, 1] * 1j ]) # on reforme un tableau numpy de complexes pour la sortie

    if but==True:
        nouveau_temps=temps_initial_iso+ min(tab_t)

    return ptn_cplx, nouveau_temps,  but, indice


# ************************************   Initialisations      **********************************************************
tic = time.time()

angle_objectif = 45
dico = {}

t = time.localtime()
instant = time.time()
filename=chargement_grib()
tig, GR = ouverture_fichier(filename)
temps=instant

# Depart
latitude_d = '46-51-00-N'
longitude_d = '04-43-00-W'


# Arrivee magellan
# latitude_a = '36-34-22-N'
# longitude_a = '06-18-00-W'

# Arrivee ag2r
latitude_a = '21-36-00-N'
longitude_a = '42-44-00-W'




d = chaine_to_dec(latitude_d, longitude_d)  # conversion des latitudes et longitudes en tuple
a = chaine_to_dec(latitude_a, longitude_a)

D = cplx(d)  # transformation des tuples des points en complexes
A = cplx(a)

# Initialisation du tableau des points d'isochrones
isochrone  = [[D.real, D.imag, 0, 0, 0, deplacement(D, A)[0], deplacement(D, A)[1]]]
isochrone2 = [[D.real, D.imag, 0, 0, 0, deplacement(D, A)[0], deplacement(D, A)[1]]]

dt1 = np.ones(6)*3600                    # intervalles de temps toutes les 10mn pendant une heure puis toutes les heures
dt2 = np.ones(378)*3600
intervalles=np.concatenate(([instant-tig],dt1,dt2))
temps_cumules=np.cumsum(intervalles)




print ('Depart : Latitude {:4.2f}  Longitude {:4.2f}'.format( d[1] , d[0]) )
print ('Arrivee: Latitude {:4.2f}  Longitude {:4.2f}'.format( a[1] , a[0]) )


# ************************************* Grib   *************************************************************************



instant_formate = time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(instant))
vit_vent_n, angle_vent = prevision(tig, GR, instant, D.imag, D.real)

# Impression des resultats
print('Date et Heure du grib  en UTC  :', time.strftime(" %d %b %Y %H:%M:%S ", time.gmtime(tig)))
print('\nLe {} heure locale Pour latitude {:6.2f} et longitude{:6.2f} '.format(instant_formate,D.real, D.imag ))
print('\tVitesse du vent {:6.3f} Noeuds'.format(vit_vent_n))
print('\tAngle du vent   {:6.1f} °'.format(angle_vent))
print()




# ***********************************Calcul des isochrones et Trace du graphique ********************************************
plt.figure('trace2')
plt.xlabel('Longitudes')
plt.ylabel('Latitudes')
plt.title('Route à suivre')

plt.xlim(-10 + min(D.real, A.real), max(D.real, A.real) + 10)  # Définit les limites du graphique en x
plt.ylim(   - (max(D.imag, A.imag) + 10 )         ,   -( -10 + min(D.imag, A.imag))                    )  # Définit les limites du graphique en y
plt.grid(True)

plt.plot(D.real, -D.imag, 'bo')  # marqueur bleu rond depart
plt.plot(A.real, -A.imag, 'ro')  # marqueur rouge arrivee

# **********************************************************************************************************************
# **********************************************************************************************************************
#on initialise l'isochrone de depart
pt1_cpx = np.array([[D]])

# tant que le but n'est pas atteint on calcule des isochrones
but = False
while but == False:
    pt1_cpx, temps, but, indice = f_isochrone(pt1_cpx, temps)

# et on on les trace
    #plt.plot(pt1_cpx[0].real, -pt1_cpx[0].imag, color = 'red', linewidth = 1)
    plt.scatter(pt1_cpx[0].real, -pt1_cpx[0].imag, c='r',s=1)



# retracage chemin à l'envers
a = int(indice)                 # indice du point de la route la plus courte
n=int(isochrone[-1][2])         # nombre d'isochrones

# on reconstitue la route à suivre en remontant le chemin
route=[]
for i in range(n):
    a = int(dico[a])
    route.append(a)      # route contient les indices successifs des points a emprunter a l'envers
route.reverse()

#on stocke les valeurs des points dans chemin
chemin = np.zeros(len(route)+1, dtype=complex)  # on initialise le np array de complexes qui va recevoir les donnees
i=0
for n in (route):
    chemin[i]=isochrone[n][0]+isochrone[n][1]*1j
    i+=1
chemin[i]=A

# maintenant on reconstitue le chemin avec les caps les TWA et les previsions
l=len(chemin)
temps_cum=temps_cumules[:l]
#previsions meteo aux differents points
vitesse1, angle_vent1=prevision_tableau2 (GR,temps_cum,chemin)

#distance et angle d un point au suivant
distance,cap1=deplacement2(chemin[0:-1],chemin[1:])

#on rajoute un 0 pour la distance arrrivee et l angle arrivee
dist=np.append(distance,[0])
caps1=np.append(cap1,[0])

# calculs twa
twa1=twa(caps1, angle_vent1)

print('vitesse1',vitesse1.shape)
print('angle_vent1',angle_vent1.shape)

print('caps1',caps1.shape)

#polaires10=polaire2_vect(polaires,vitesse1,angle_vent1,caps1)
#print ('polaires\n',polaires10)

temps_cum+=tig
#mise en forme pour concatener
chx=chemin.real.reshape((1, -1))
chy=chemin.imag.reshape((1, -1))
temps_pts=temps_cum.reshape((1, -1))
vitesse=vitesse1.reshape((1, -1))
angle_vent= angle_vent1.reshape((1, -1))
cap= caps1.reshape((1, -1))
twa= twa1.reshape((1, -1))

#print('twa',twa)

#tabchemin : x,y,vit vent ,angle_vent,cap vers point suivant twa vers point suivant
chem=np.concatenate((chx.T,chy.T,temps_pts.T,vitesse.T,angle_vent.T,cap.T,twa.T),axis=1)
#print ('tabchemin \n',chem)

indexiso=np.arange(l)
df = pd.DataFrame(chem, index = indexiso, columns = ['x', 'y', 't', 'vitesse_v','angle_v','cap','twa'])
print(df.head(5))
df.to_csv('fichier_panda.csv')
#print ('tabchemin.shape',chem.shape)
print ('\t n \t\t\t Date \t\t\t\t  X \t\t\tY  \tV_vent \t A_Vent \tCap \tTWA')
for i in range (len(chem)):
    print('\t {}  \t{} \t{:6.3f} \t{:6.3f}\t{:6.2f} \t{:6.0f} \t{:6.0f} \t{:6.1f}'.format( i,
    time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(chem[i,2])),chem[i,0],chem[i,1],chem[i,3],chem[i,4],chem[i,5],chem[i,6]))

duree=(temps-instant)[0]
print ('temps total en s ',duree)
j= duree//(3600*24)
h=(duree-(j*3600*24))//3600
mn=(duree-(j*3600*24)-h*3600)//60

print ('temps total {} j {} h {} mn'.format(j,h,mn))

plt.plot(chemin.real,-chemin.imag,'k')   # trace du chemin"



#   ****************************************Controle du temps dexecution **********************************
tac = time.time()
print('\nDuree d\'execution:  {:4.2f} s'.format(tac - tic))
plt.show()

