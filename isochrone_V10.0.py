#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 08:52:41 2019

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
from polaires_imoca import *
from operator import itemgetter

tic = time.time()

# *****************************************   Donnees   ****************************************************************


# dans tous les calculs la longitude correspondant à l'axe des x est prise en premier
# Les points sont definis en longitude latitude
# Attention les previsions sont elles faites en latitude longitude
# les latitudes sont positives vers le sud et les longitudes positives vers l'est
# Les points initiaux sont sous forme de tuple longitude latitude
# les angles sont des angles trigo
# pour le vent on parle de vitesses et angles




angle_objectif = 45
angle_twa_pres = 40
angle_twa_ar = 20
delta_temps = 3600  # duree du deplacement en s: temps entre 2 isochrones

dico = {}


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


def cplx(D):
    ''' transforme un tuple en nparray complex'''
    dc = np.array(D[0] + D[1] * 1j)
    return dc


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
    points_arrivee = np.zeros((range.shape),   dtype=complex)  # Init tableau   points d'arrivee sous forme complexe
    range_radian = (-range + 90) * math.pi / 180
    vit_noeuds = polaire2_vect(polaires, vit_vent, angle_vent, range)  # Vitesses suivant les differents caps

    points_arrivee = D + (d_t / 3600 / 60 * vit_noeuds * (
            np.cos(range_radian) / math.cos(D.imag * math.pi / 180) + np.sin(range_radian) * 1j))
    # print('cos du deplacement',np.cos(range_radian))
    return points_arrivee, tp + d_t


def deplacement(D, A):
    '''retourne la distance et l'angle du deplacement entre le depart et l'arrivee'''
    C = A - D
    return np.abs(C), (90 - np.angle(C, deg=True))


def rangenavi(capa, capb):
    if capb > capa:
        range = np.arange(capa, capb)
    else:
        range = np.concatenate((np.arange(0, capb + 1), np.arange(capa, 360)), axis=0)
    return range


def range_cap(direction_objectif, direction_vent, a_vue_objectif, angle_pres, angle_var):
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


def f_isochrone(pt_init_cplx, temps_initial_iso, isochrone):
    ''' Calcule le nouvel isochrone a partir d'un tableau de points pt2cplx tableau numpy de cplx'''
    ''' deltatemps, tig , U, V sont supposees etre des variables globales'''
    ''' Retourne les nouveaux points el le nouveau temps et implemente le tableau general des isochrones'''

    but = False
    points_calcul = []
    caps_x = []
    tab_t = []  # tableau des temps vers l arrivee en ligne directe
    delta_temps = 3600/3
    numero_iso = int(isochrone[-1][2] + 1)
    numero_dernier_point = (isochrone[-1][4])  # dernier point isochrone precedent
    numero_premier_point = isochrone[-1][4] - pt_init_cplx.size
    t_iso_formate = time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(temps_initial_iso+delta_temps))

    print(' Isochrone N° {} heure {}'.format(numero_iso,t_iso_formate)  )

    for i in range(pt_init_cplx.size):
        vit_vent, angle_vent = prevision(tig,GR, temps_initial_iso, pt_init_cplx[i].imag, pt_init_cplx[
            i].real)  # Calcul  prevision meteo au point  i et au temps_initial_iso
        range_caps = range_cap(deplacement(pt_init_cplx[i], A)[1], angle_vent, angle_objectif, angle_twa_pres,
                               angle_twa_ar)  # Calcul des caps a etudier

        n_pts_x, nouveau_temps = calcul_points(pt_init_cplx[i], temps_initial_iso, delta_temps, angle_vent, vit_vent,
                                               range_caps, polaires)  # Calcul de la nouvelle serie generale de points

#  il faut garder en memoire le cap suivi ou le recalculer ensuite
#***********************************************************************************************************************


        # la tous les nouveaux points sont calcules maintenant on expurge et on stocke
        for j in range(len(n_pts_x)):
            cap_arrivee = deplacement(n_pts_x[j], A)[1]
            distance_arrivee = deplacement(n_pts_x[j], A)[0]
            points_calcul.append(
                [n_pts_x[j].real, n_pts_x[j].imag, numero_iso, numero_premier_point + i + 1, 1, distance_arrivee,
                 cap_arrivee])

            caps_x.append(cap_arrivee)
    # print('max caps ', max(caps_x))
    # print('min caps ', min(caps_x))
    coeff2 = 50 / (max(caps_x) - min(caps_x))  # coefficient pour ecremer et garder 50 points

    for j in range(len(points_calcul)):  # partie ecremage
        points_calcul[j][6] = int(coeff2 * points_calcul[j][6])

    pointsx = sorted(points_calcul, key=itemgetter(6, 5))  # tri de la liste de points suivant la direction (indice  " \
    pointsx =np.asarray(pointsx)
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
        t_a = 60 * d_a / resultat
        tab_t.append(t_a)
        # print('temps',t_a)
        if t_a < delta_temps / 3600:
            but = True
        # indice du temps minimum

    # print('temps minimum', min(tab_t))
    indice = tab_t.index(min(tab_t)) + numero_dernier_point + 1
    # print('indice de temps minimum', indice)
    # print (' numero global du point ',indice+numero_dernier_point+2)
    # print('\nPoint correspondant', pointsx[indice])
    # print()

    # print ('{} points'.format(pointsx.shape[0]))
    isochrone = np.concatenate((isochrone, pointsx))  # On rajoute ces points a la fin du tableau isochrone
    ptn_cplx = pointsx[:, 0] + pointsx[:, 1] * 1j  # on reforme un tableau numpy de complexes pour la sortie
    # print('{} Points  de l isochrone \n {}'.format(ptn_cplx.size, ptn_cplx))
    return ptn_cplx, nouveau_temps, isochrone, but, indice





# ************************************   Fin des Fonctions   **********************************************************

# ************************************   Initialisations      **********************************************************

# 1 : x , 2 y du point , 3 N°iso, 4 N° pt mere , 5 N° pt , 6 distance a l'arrivee , 7 cap a l'arrivee, 8 polaire depuis le pt precedent , 9 twa depuis le point precedent , 10 cap depuis le point precedent





# Depart
latitude_d = '15-33-00-N'
longitude_d = '68-31-00-W'

# Arrivee
latitude_a = '12-10-00-N'
longitude_a = '68-56-00-W'

d = chaine_to_dec(latitude_d, longitude_d)  # conversion des latitudes et longitudes en tuple
a = chaine_to_dec(latitude_a, longitude_a)

D = cplx(d)  # transformation des tuples des points en complexes
A = cplx(a)
Depart = np.array([[d[0] + d[1] * 1j]])    # le depart est mis sous forme d'un tableau complexe
# Initialisation du tableau des points d'isochrones
isochrone  = [[D.real, D.imag, 0, 0, 0, deplacement(D, A)[0], deplacement(D, A)[1]]]
isochrone2 = [[D.real, D.imag, 0, 0, 0, deplacement(D, A)[0], deplacement(D, A)[1]]]

print ('depart',d)
print ('arrivee',a)

# ************************************* Grib   *************************************************************************

t = time.localtime()
instant = time.time()
filename=chargement_grib()
tig, GR = ouverture_fichier(filename)



instant_formate = time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(instant))
vit_vent_n, angle_vent = prevision(tig, GR, instant, d[1], d[0])


# Impression des resultats
print('Date et Heure du grib  en UTC  :', time.strftime(" %d %b %Y %H:%M:%S ", time.gmtime(tig)))
print('\nLe {} heure locale Pour latitude {:6.2f} et longitude{:6.2f} '.format(instant_formate,d[1], d[0] ))
print('\tVitesse du vent {:6.3f} Noeuds'.format(vit_vent_n))
print('\tAngle du vent   {:6.1f} °'.format(angle_vent))
print()




# ***********************************Calcul des isochrones et Trace du graphique ********************************************
plt.figure('trace2')
plt.xlabel('Longitudes')
plt.ylabel('Latitudes')
plt.title('Route A suivre')

# limy=(min(d[1],a[1]),max(d[1],a[1]))

plt.xlim(-10 + min(d[0], a[0]), max(d[0], a[0]) + 10)  # Définit les limites du graphique en x
plt.ylim(   - (max(d[1], a[1]) + 10 )         ,   -( -10 + min(d[1], a[1]))                    )  # Définit les limites du graphique en y
plt.grid(True)

plt.plot(d[0], -d[1], 'bo')  # marqueur bleu rond depart
plt.plot(a[0], -a[1], 'ro')  # marqueur rouge arrivee

# **********************************************************************************************************************
# **********************************************************************************************************************
pt1_cpx = Depart
temps=instant
but = False
while but == False:
    pt1_cpx, temps, isochrone, but, indice = f_isochrone(pt1_cpx, temps, isochrone)
    #print ('pt1_cpx.shape',pt1_cpx.shape)
    plot2 = plt.plot(pt1_cpx.real, -pt1_cpx.imag, color = 'red', linewidth = 1)      # Tracage isochrone





# retracage chemin
a = int(indice)                 #indice du point de la route la plus courte
plt.plot(isochrone[a][0], -isochrone[a][1], 'k.')  # trace de l'arrivee
n=int(isochrone[-1][2])

#print('\nRoute à suivre')

route=[]
for i in range(n):
    a = int(dico[a])
    route.append(a)      # route contient les indices successifs des points a emprunter a l'envers

#print('route',route)
route.reverse()
#print ('reverse',route)

chemin = np.zeros(len(route), dtype=complex)  # initialise le np array de complexes qui recoit les donnees

pointsx=[]
pointsy=[]
for i in range(len(route)):
    n=route[i]
    pointsx.append(isochrone[n][0])
    pointsy.append(-isochrone[n][1])
    #print ('points:{} x={} y={}'.format(n,isochrone[n][0],-isochrone[n][1]))

plt.plot(pointsx,pointsy)

#   ****************************************Controle du temps dexecution **********************************
tac = time.time()
print('\nDuree d\'execution:  {:4.2f} s'.format(tac - tic))
plt.show()