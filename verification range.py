
import numpy as np

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
    print('cap1',cap1)
    cap2 = (direction_vent - angle_pres ) % 360
    print('cap2', cap2)
    cap3 = (180 + direction_vent + angle_var) % 360
    print('cap3', cap3)
    cap4 = (180 + direction_vent - angle_var ) % 360
    print('cap4', cap4)
    cap5 = (direction_objectif - a_vue_objectif) % 360
    print('cap5', cap5)
    cap6 = (direction_objectif + a_vue_objectif) % 360
    print('cap6', cap6)


    z1 = rangenavi(cap1, cap4)
    print('z1',z1)
    print()
    z2 = rangenavi(cap3, cap2)
    print('z2', z2)
    z3 = rangenavi(cap5, cap6)
    print('z3', z3)
    range1 = np.intersect1d(z1, z3)
    range2 = np.intersect1d(z2, z3)

    rangetotal = np.concatenate((range1, range2), axis=0)
    return rangetotal


direction_objectif=90
direction_vent=90

a_vue_objectif=90
angle_pres=45
angle_var=20

rangec= range_cap(direction_objectif, direction_vent, a_vue_objectif, angle_pres, angle_var)

def twa(cap, dvent):
    twa = 180 - abs(((360 - dvent + cap) % 360) - 180)
    return twa
print()
print()
print ('range',rangec)
print()

for i in range(len(rangec)):
    twa = 180 - abs(((360 - direction_vent + rangec[i]) % 360) - 180)

    print(rangec[i],' ',twa)


#TWA =twa(rangec,direction_vent)

#print ('TWA',TWA)