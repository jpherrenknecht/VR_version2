# Source
# # # http://toxcct.free.fr/polars/generator.htm
# # # http://toxcct.free.fr/polars/help/csvgen_input.htm
# # # pour obtenir les donnees brutes dans vr dashboard raw values reperer la ligne et la copier
# copies des donnees brutes - retirer tWA TWS le replacer par 0, remplacer les ; par des , - ajouter   : ],[ à la fin de chaque ligne, polaires=np.array([[ au debut et ]])


import numpy as np
import math





polaires=np.array([[
0,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,50,60,70],[
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[
30,0,2.738,5.326,7.482,8.927,9.067,10.07,10.501,10.662,10.802,10.923,11.063,11.204,11.344,11.344,11.484,11.484,11.264,10.852,9.468,8.335],[
35,0,3.169,6.62,9.218,10.943,11.093,12.527,12.808,13.099,13.24,13.48,13.621,13.902,14.042,14.042,14.182,14.323,14.042,13.53,11.765,10.321],[
40,0,4.022,8.064,11.234,13.24,13.681,15.256,15.687,15.978,16.259,16.449,16.74,16.88,17.021,17.161,17.302,17.442,17.091,16.479,14.323,12.688],[
45,0,4.453,8.927,12.237,14.112,14.403,15.837,16.409,16.85,17.282,17.302,17.583,17.723,18.004,18.144,18.295,18.576,18.214,17.563,15.216,13.43],[
50,0,4.754,9.639,12.949,14.112,14.975,16.409,17.131,17.563,17.994,18.144,18.435,18.716,18.997,19.137,19.569,20,19.599,18.897,16.369,14.554],[
55,0,5.045,10.361,13.681,14.403,15.546,17.131,17.563,18.285,18.716,18.856,19.137,19.709,20,20.281,20.702,21.404,20.983,20.231,17.512,15.546],[
60,0,5.326,10.802,14.253,14.975,15.978,17.563,18.285,18.856,19.288,19.569,20,20.421,20.842,21.404,21.835,22.828,22.377,21.575,18.666,16.549],[
65,0,5.577,11.023,14.594,15.446,16.309,17.883,18.736,19.308,20.03,20.471,21.123,21.695,22.257,22.828,23.4,24.814,24.323,23.45,20.331,18.034],[
70,0,5.847,11.404,14.824,15.677,16.68,18.525,19.097,19.96,20.662,21.494,22.116,22.979,23.54,24.383,24.955,26.941,26.409,25.456,22.116,19.528],[
75,0,5.988,11.545,15.105,16.239,17.101,18.881,20.047,20.932,21.945,22.794,23.653,24.298,25.167,25.894,26.763,28.932,27.803,26.8,23.27,20.521],[
80,0,6.128,11.825,15.246,17.101,17.392,19.25,20.726,22.083,23.116,24.138,25.004,25.859,26.693,27.58,28.602,30.97,29.187,28.134,24.413,21.645],[
85,0,6.128,11.825,15.386,17.392,18.094,19.533,21.158,22.677,24.013,25.317,26.328,27.497,28.498,29.197,30.084,32.139,30.301,29.207,25.316,22.397],[
90,0,6.128,11.825,15.386,17.532,18.666,20.119,21.743,23.262,24.899,26.349,27.664,28.967,29.833,30.678,31.408,33.328,31.414,30.281,26.339,23.26],[
95,0,5.988,11.545,15.246,17.392,18.947,20.402,22.174,24.159,25.786,27.392,28.55,29.718,30.574,31.127,31.554,34.068,31.133,30.02,26.088,23.009],[
100,0,5.847,11.404,14.824,17.101,19.097,20.544,22.472,24.753,26.537,28.279,29.447,30.595,31.158,31.575,31.992,34.214,31.133,30.02,26.088,23.009],[
105,0,5.557,10.973,14.684,17.252,18.947,20.686,22.616,25.045,26.829,28.728,29.593,30.595,31.304,32.013,32.597,34.506,32.246,31.083,26.981,23.881],[
110,0,5.286,10.692,14.684,17.392,18.666,20.686,22.76,25.494,27.424,29.166,29.739,30.595,31.304,32.305,33.328,35.55,33.5,32.297,27.994,24.754],[
115,0,5.186,10.662,14.624,17.101,18.666,20.544,22.904,25.494,27.278,29.02,29.885,31.043,32.045,33.056,34.193,36.718,34.614,33.36,28.886,25.627],[
120,0,5.186,10.361,14.403,17.131,18.967,20.402,22.904,25.494,27.132,28.874,30.188,31.481,32.785,33.933,35.08,37.751,35.576,34.303,29.789,26.369],[
125,0,4.895,9.789,13.972,16.7,18.716,20.605,23.284,25.494,27.132,28.874,30.334,31.627,33.088,34.381,35.675,38.794,36.559,35.245,30.561,27.001],[
130,0,4.754,9.358,13.24,16.118,18.285,20.605,23.294,25.744,27.403,28.874,30.48,31.919,33.526,34.819,36.269,39.67,37.392,36.048,31.193,27.613],[
135,0,4.313,8.495,12.377,15.256,17.422,19.584,22.4,25.15,26.808,29.082,30.762,32.368,33.818,35.257,36.707,41.026,38.786,37.382,32.467,28.736],[
140,0,4.022,7.924,11.514,14.403,16.7,18.714,21.23,24.555,26.193,29.197,30.824,32.597,34.068,35.55,37.01,42.768,40.311,38.856,33.751,29.859],[
145,0,3.45,7.192,10.361,13.099,15.546,17.561,19.751,22.604,24.701,27.434,29.792,32.295,34.36,36.134,37.897,42.476,40.04,38.585,33.5,29.609],[
150,0,3.169,6.329,9.358,12.237,14.543,16.54,18.724,20.967,23.355,25.953,28.905,31.992,34.506,36.718,38.94,42.184,39.749,38.325,33.239,29.358],[
155,0,2.879,5.757,8.355,11.093,13.24,15.529,17.542,19.611,21.707,23.741,26.401,29.197,31.846,34.068,36.572,41.579,39.197,37.783,32.728,28.987],[
160,0,2.598,5.045,7.633,10.07,12.377,14.518,16.505,18.568,20.351,21.676,24.336,26.986,29.499,31.992,34.36,40.849,38.505,37.111,32.216,28.485],[
170,0,2.307,4.754,7.192,9.498,11.514,13.38,14.975,16.7,18.285,19.569,21.835,23.962,26.379,28.505,30.762,36.439,35.717,33.6,29.919,26.369],[
180,0,2.166,4.614,6.76,9.067,11.093,12.808,14.403,15.978,17.422,18.716,20.842,23.119,25.235,27.502,29.498,35.165,34.473,30.14,28.194,25.496]])

# ************************************************Fonctions   **********************************************************

def twa(cap, dvent):
    twa = 180 - abs(((360 - dvent + cap) % 360) - 180)
    return twa

def polaire (polaires,vent,twa):
    # Recherche des indices
    i,j=0,0
    while i < np.size(polaires[0]):
        if vent < polaires[0][i]:
            break
        i+= 1
    while j < np.size(polaires[:,0]):
        if twa < polaires[j][0]:
            break
        j+= 1


    dx=vent-polaires[0][i-1]
    dy=twa-polaires[j-1][0]
    deltax=polaires[0][i]-polaires[0][i-1]
    deltay=polaires[j][0]-polaires[j-1][0]

    # print('dx',dx)
    # print('dy',dy)
    # print('deltax',deltax)
    # print('deltay',deltay)


    fx1y1=polaires[j-1][i-1]
    fx1y2=polaires[j][i-1]
    fx2y1=polaires[j-1][i]
    fx2y2=polaires[j][i]

    # print ('fx1y1',fx1y1)
    # print ('fx1y2',fx1y2)
    # print ('fx2y1',fx2y1)
    # print ('fx2y2',fx2y2)


    deltafx=fx2y1-fx1y1
    deltafy=fx1y2-fx1y1
    deltafxy=fx1y1+fx2y2-fx2y1-fx1y2

    # print ('deltafx',deltafx)
    # print ('deltafy',deltafy)
    # print ('deltafxy',deltafxy)

    resultat=(deltafx*dx/deltax)+(deltafy*dy/deltay)+(deltafxy*dx*dy/deltax/deltay)+fx1y1

    return resultat


def polaire2(polaires,vit_vent,angle_vent,cap):
    twa = 180 - abs(((360 - angle_vent + cap) % 360) - 180)
    # Recherche des indices
    i,j=0,0
    while i < np.size(polaires[0]):
        if vit_vent < polaires[0][i]:
            break
        i+= 1
    while j < np.size(polaires[:,0]):
        if twa < polaires[j][0]:
            break
        j+= 1

    dx = vit_vent - polaires[0][i - 1]
    dy = twa - polaires[j - 1][0]
    deltax = polaires[0][i] - polaires[0][i - 1]
    deltay = polaires[j][0] - polaires[j - 1][0]
    fx1y1 = polaires[j - 1][i - 1]
    fx1y2 = polaires[j][i - 1]
    fx2y1 = polaires[j - 1][i]
    fx2y2 = polaires[j][i]
    deltafx = fx2y1 - fx1y1
    deltafy = fx1y2 - fx1y1
    deltafxy = fx1y1 + fx2y2 - fx2y1 - fx1y2

    resultat = (deltafx * dx / deltax) + (deltafy * dy / deltay) + (deltafxy * dx * dy / deltax / deltay) + fx1y1

    return resultat

def polaire2_vect(polaires,vit_vent,angle_vent,tableau_caps):
    '''A partir du tableau des polaires du bateau retourne les polaires suivant les caps et le vent'''
    polaires2=np.zeros(len(tableau_caps))
    for k in range(len(tableau_caps)):
        twa = 180 - abs(((360 - angle_vent + tableau_caps[k]) % 360) - 180)
        #print(twa)
        # Recherche des indices
        i,j=0,0
        while i < np.size(polaires[0]):
            if vit_vent < polaires[0][i]:
                break
            i+= 1
        while j < np.size(polaires[:,0]):
            if twa < polaires[j][0]:
                break
            j+= 1
        dx = vit_vent - polaires[0][i - 1]
        dy = twa - polaires[j - 1][0]
        deltax = polaires[0][i] - polaires[0][i - 1]
        deltay = polaires[j][0] - polaires[j - 1][0]
        fx1y1 = polaires[j - 1][i - 1]
        fx1y2 = polaires[j][i - 1]
        fx2y1 = polaires[j - 1][i]
        fx2y2 = polaires[j][i]
        deltafx = fx2y1 - fx1y1
        deltafy = fx1y2 - fx1y1
        deltafxy = fx1y1 + fx2y2 - fx2y1 - fx1y2

        polaires2[k] = (deltafx * dx / deltax) + (deltafy * dy / deltay) + (deltafxy * dx * dy / deltax / deltay) + fx1y1

    return polaires2

#pol_vect=np.vectorize (polaire2)



if __name__=='__main__':
    vit_vent = 25
    angle_vent = 100
    cap=140
    tableau_caps = np.array([140, 141, 142])
    twa = 180 - abs(((360 - angle_vent + cap) % 360) - 180)

# premiere fonction
    resultat=polaire(polaires,vit_vent,twa)
    print('\n\tPolaire pour un Vent de {} Noeuds  et une twa de {}° = {:6.3f} Noeuds '.format(vit_vent,twa, resultat))

# deuxieme fonction
    res=polaire2(polaires,vit_vent,angle_vent,cap)
    print ('\tPour un vent de {} Noeuds avec une twa de {}° la polaire est {}'.format(vit_vent,twa,res))

#troisieme fonction
    res=polaire2_vect(polaires,vit_vent,angle_vent,tableau_caps)
    print(res)

# quatrieme fonction ne marche pas
#     res = pol_vect(polaires, vit_vent, angle_vent, tableau_caps)
#     print(res)