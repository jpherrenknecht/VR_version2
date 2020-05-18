import numpy as np
import math

A=np.array(([160,200,280],[10,20,340],[40,350,30]))




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

def interpol_circ(start,end,ratio):
    result = (start + (((((end - start) % 360) + 540) % 360) - 180) * ratio) % 360
    return result



start=350
end=40
ratio=0.1
test=interpol_circ(start,end,ratio)
print ('Par fonction',test)



