# test
import os
import time
import math
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
from Uploadgrib import *
# from polaires_imoca import *
from polaires_figaro2 import *
from operator import itemgetter

tic = time.time()


def rangenavi(capa, capb):
    if capb > capa:
        range = np.arange(capa, capb, 1)
    else:
        range = np.concatenate((np.arange(0, capb + 1, 1), np.arange(capa, 360, 1)), axis=0)
    return range

def range_cap(direction_objectif, direction_vent, a_vue_objectif, angle_pres, angle_var):
    # print ('direction_vent indice i',direction_vent)
    # print('direction_objectif indice i', direction_objectif)
    direction_vent, direction_objectif = int(direction_vent), int(direction_objectif)
    cap1 = (direction_vent + angle_pres) % 360
    cap2 = (direction_vent - angle_pres ) % 360
    cap3 = (180 + direction_vent + angle_var) % 360
    cap4 = (180 + direction_vent - angle_var ) % 360
    cap5 = (direction_objectif - a_vue_objectif) % 360
    cap6 = (direction_objectif + a_vue_objectif) % 360
    z1 = rangenavi(cap1, cap4)
    z2 = rangenavi(cap3, cap2)
    z3 = rangenavi(cap5, cap6)
    range1 = np.intersect1d(z1, z3)
    range2 = np.intersect1d(z2, z3)
    rangetotal = np.concatenate((range1, range2), axis=0)
    return rangetotal

def dist_cap(D, A):
    '''retourne la distance et l'angle du deplacement entre le depart et l'arrivee'''
    C = A - D
    return np.abs(C), (450 + np.angle(C, deg=True)) % 360

def twa(hdg, twd):
    '''retourne la twa a partir de la direction du vent et du cap'''
    '''Peut fonctionner avec des np.array'''
    twa = 180 - abs(((360 - twd + hdg) % 360) - 180)
    return twa


def deplacement(D, d_t, hdg, vT):
    '''D Depart point complexe ,d_t duree en s  , hdg cap en° ,vT vitesse Polaire en Noeuds'''
    hdg_r = hdg * math.pi / 180
    A = D + (d_t / 3600 / 60 * vT * (np.sin(hdg_r) / math.cos(D.imag * math.pi / 180) - np.cos(hdg_r) * 1j))
    return A


def deplacement2(D, d_t, HDG, VT):
    '''D Depart point complexe ,d_t duree en s  , HDG tableau de caps en° ,vT Tableau de vitesses Polaires en Noeuds'''
    '''Fonctionne avec des np.array'''
    HDG_R = HDG * math.pi / 180
    A = D + (d_t / 3600 / 60 * VT * (np.sin(HDG_R) / math.cos(D.imag * math.pi / 180) - np.cos(HDG_R) * 1j))
    return A


def calcul_points(D,tp, d_t,twd, tws, HDG, VT):
    '''D point de depart ,tp temps au point D; d_t duree du deplacement en s ; twd angle du vent au point ;
    tws Vitesse du vent au point ; HDG np.array de caps a simuler  ; HDG np.array de polaires du bateau
    retourne un tableau points sous forme de valeurs complexes'''
    VT = polaire2_vect(VT, tws, twd, HDG)  # Vitesses suivant les differents caps
    points_arrivee = deplacement2(D, d_t, HDG, VT)
    return points_arrivee, tp + d_t


def calcul_points2(D, tp, d_t, twd, tws, HDG, polaires):
    ''' D point de depart; d_t duree du deplacement en s ; angle du vent au point ; Vitesse du vent au point ; caps a simuler  ; polaires du bateau  '''
    '''retourne un tableau points sous forme de valeurs complexes'''
    points_arrivee = np.zeros((HDG.shape), dtype=complex)  # Init tableau   points d'arrivee sous forme complexe
    range_radian = (-HDG + 90) * math.pi / 180
    vit_noeuds = polaire2_vect(polaires, tws, twd, HDG)  # Vitesses polaires suivant les differents caps

    points_arrivee = D + (d_t / 3600 / 60 * vit_noeuds * (
                np.cos(range_radian) / math.cos(D.imag * math.pi / 180)
                - np.sin(range_radian) * 1j))
    return points_arrivee, tp + d_t


#**********************************************************************************************************************



def f_isochrone(pts_init_cplx, temps_initial_iso):
    ''' Calcule le nouvel isochrone a partir d'un tableau de points pt2cplx tableau numpy de cplx'''
    ''' deltatemps, tig , U, V sont supposees etre des variables globales'''
    ''' Retourne les nouveaux points el le nouveau temps et implemente le tableau general des isochrones'''
    global isochrone, intervalles, t_v_ar_h
    numero_iso = int(isochrone[-1][2] + 1)
    delta_temps = intervalles[numero_iso]  # Ecart de temps entre anciens points et nouveaux en s
    t_iso_formate = time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(temps_initial_iso + delta_temps))

    # on recupere toutes les previsions meteo d'un coup pour l'ensemble des points de depart
    print ('tig et t initial iso ',tig,temps_initial_iso)
    print('ecart en h ',(-tig+temps_initial_iso)/3600 )

    TWS,TWD = prevision_tableau(tig, GR, temps_initial_iso, pts_init_cplx)
    # impressionpour test
    #print ('TWS\n',TWS)
    #print ('TWD\n',TWD)

    #pour chaque point
    for i in range(pts_init_cplx.size):
    #recherche des caps possibles vers objectif
        HDG=range_cap(dist_cap(pts_init_cplx[0][i],A)[1], TWD[i],angle_objectif, angle_pres, angle_var)
        TWA=twa(HDG,TWD[i])
        if (min(TWA) < angle_pres - 1):
            print('Problème de TWA')
        else:
            print('pas de pb de TWA')
        print ('valeur pour un point',TWS[i], TWD[i], HDG)

    # calcul des polaires vT
        VT=polaire2_vect(polaires, TWS[i], TWD[i], HDG)
        print ('VT',VT)
    #calcul des nouveaux points

        print('pt de depart',pts_init_cplx[0][i])
        print(pts_init_cplx[0][i].dtype)
        print(' temps_initial_iso',temps_initial_iso)
        print('TWD[i]',TWD[i])
        print('TWS[i]', TWS[i])
        deplacement2(pts_init_cplx[0][i], delta_temps, HDG, VT)

      #  n_pts_x, nouveau_temps=calcul_points(pts_init_cplx[0][i], temps_initial_iso, delta_temps, TWD[i],TWS[i] , HDG, VT)

       # print ('Nouveaux points\n ',n_pts_x)




    but = False
    points_calcul = []
    caps_x = []
    tab_t = []  # tableau des temps vers l arrivee en ligne directe
    print(' Isochrone N° {}  {}'.format(numero_iso, t_iso_formate))
    numero_dernier_point = (isochrone[-1][4])  # dernier point isochrone precedent
    numero_premier_point = isochrone[-1][4] - pts_init_cplx.size

    # on recupere toutes les previsions meteo d'un coup pour l'ensemble des points de depart
    vit_vent, angle_vent = prevision_tableau(tig, GR, temps_initial_iso, pts_init_cplx)

    return None


if __name__ == '__main__':
    angle_objectif = 90

    latitude_d = '30-00-00-N'      # Depart
    longitude_d = '15-00-00-W'
    latitude_a = '15-00-00-N'      # Arrivee
    longitude_a = '30-00-00-W'

    d = chaine_to_dec(latitude_d, longitude_d)  # conversion des latitudes et longitudes en tuple
    a = chaine_to_dec(latitude_a, longitude_a)
    D = d[0] + d[1] * 1j  # transformation des tuples des points en complexes
    A = a[0] + a[1] * 1j

    print('\nDepart : Latitude {:6.4f}  \tLongitude {:6.4f}'.format(d[1], d[0]))
    print('Arrivee: Latitude {:6.4f}  \tLongitude {:6.4f}'.format(a[1], a[0]))
    depl = dist_cap(D, A)
    print('cap Depart vers Arrivee {:6.2f}   distance {:6.2f}'.format(depl[1], depl[0]))

    # Initialisation du tableau des points d'isochrones
    isochrone = [[D.real, D.imag, 0, 0, 0, dist_cap(D, A)[0], dist_cap(D, A)[1]]]
    print('D',D)
    D2=-15-10*1j
    pts_init_cplx = np.array([[D  ,D2  ]])







    # On charge le grib
    filename = chargement_grib()
    tig, GR = ouverture_fichier(filename)
    print('Date et Heure du grib  en UTC  :', time.strftime(" %d %b %Y %H:%M:%S ", time.gmtime(tig)))
# prevision au depart a l'instant present
    instant_formate = time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(tic))
    vit_vent_n, angle_vent = prevision(tig, GR, tic, D.imag, D.real)
    print('\nLe {} heure locale Pour latitude {:6.2f} et longitude{:6.2f} '.format(instant_formate, D.real, D.imag))
    print('\tVitesse du vent {:6.3f} Noeuds'.format(vit_vent_n))
    print('\tAngle du vent   {:6.1f} °'.format(angle_vent))
    print()

    vit_vent_n, angle_vent = prevision(tig, GR, tic, D2.imag, D2.real)
    print('\nLe {} heure locale Pour latitude {:6.2f} et longitude{:6.2f} '.format(instant_formate, D.real, D.imag))
    print('\tVitesse du vent {:6.3f} Noeuds'.format(vit_vent_n))
    print('\tAngle du vent   {:6.1f} °'.format(angle_vent))
    print()

    dt1 = np.ones(6) * 600  # intervalles de temps toutes les 10mn pendant une heure puis toutes les heures
    dt2 = np.ones(2) * 3600   #todo le 2 sera replace par un 383 ou moins  en phase definitive
    intervalles = np.concatenate(([tic - tig], dt1, dt2))
    temps_isos = np.cumsum(intervalles)+tig


    temps_depart_iso=temps_isos[0]
    f_isochrone(pts_init_cplx, temps_depart_iso)
    # *****************************TRACE ******************************************************************





    plt.figure('trace2')
    plt.xlabel('Longitudes')
    plt.ylabel('Latitudes')
    plt.title('Route à suivre')


    plt.xlim(-10 + min(D.real, A.real), max(D.real, A.real) + 10)  # Définit les limites du graphique en x
    plt.ylim(- (max(D.imag, A.imag) + 10), -(-10 + min(D.imag, A.imag)))  # Définit les limites du graphique en y
    plt.grid(True)

    plt.plot(D.real, -D.imag, 'bo')  # marqueur bleu rond depart
    plt.plot(D2.real, -D2.imag, 'bo')  # marqueur vertond depart2
    plt.plot(A.real, -A.imag, 'ro')  # marqueur rouge arrivee


    tac = time.time()
    print('\nDuree d\'execution:  {:4.2f} s'.format(tac - tic))
    plt.show()