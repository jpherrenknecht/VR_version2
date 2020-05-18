

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


def deplacement(D, A):
    '''retourne la distance et l'angle du deplacement entre le depart et l'arrivee'''
    C = A - D
    return np.abs(C), (90 - np.angle(C, deg=True))




t = time.localtime(time.time())



print(t)
t = time.localtime(time.time()+3600)
print(t)

print ('t3',t[3])








#
# points=np.array([0+0*1j , 1+1*1j , 2+1*1j , 2+3*1j , 4+3.5*1j])
# print ('points',points)
#
# points1=points[1:]
#
# print ('points1',points1)
#
# points2=points[0:-1]
#
# print ('points2',points2)
#
#
# distance,angle=deplacement(points[0:-1],points[1:])
#
# print ('distance',distance)
# print ('angle',angle)
#
#
#
#
#
#
#
#
#
#
#
# # Depart
# latitude_d = '05-00-00-N'
# longitude_d = '10-00-00-W'
# # Arrivee
# latitude_a = '10-00-00-N'
# longitude_a = '10-00-00-W'
#
#
#
# route =[2,3,4,5,6]
#
# for el in route :
#     print (el)
#
#
#
#
#
#
# x = np.array([1, 3, 4, 6])
# y = np.array([2, 3, 5, 1])
#
# print('X',x)
# print ('X shape ',x.shape)
#
# plt.plot(x, y)
#
# #plt.show() # affiche la figure a l'ecran
#
#
#
# # print ('dt1',dt1)
# # itemp=np.concatenate((dt1,dt2))
# # print ('itemp',itemp)
# # itemp2=np.cumsum(itemp)
# # print('itemp2',itemp2)
#
# # print (intervalles)
# #
# # print(np.cumsum(intervalles))
#
# tp=150
# tig=100
#
#
# #itemp=np.ones( points.shape)*15
# # D=chaine_to_cplx(latitude_d, longitude_d)
# # A=chaine_to_cplx(latitude_a, longitude_a)
# #
# #
# #itemp = np.ones(points.shape) * (tp - tig) / 3600 / 3
#
#
# #dt3 =np.concatenate((  np.ones((2,1))*10, np.ones((2,1))*100))
# dt3 =np.concatenate(([0], np.ones(2)*10, np.ones(1)*100))
# dt4=np.cumsum(dt3)
# print('dt4',dt4)
#
# dt5=dt4.reshape((1,-1))
#
# point=np.array([-10-2*1j, -5+3*1j , 0+10*1j , 10 +20*1j])
# print ('points.shape',point.shape)
# points=point.reshape((1,-1))
#
# ilati = np.imag(points) + 90
# ilong = np.real(points) % 360
#
# e = np.concatenate((dt5.T, ilati.T, ilong.T), axis=1)
#
# print('e\n',e)
#
#
# print()
# g=np.arange(10)
# print(g)
# h=g[:5]
# print('h',h)
#
#
# points=np.array([
# -68.51666 -15.555*1j,
# -68.515375-15.5514*1j,
# -68.51408  -15.478*1j,
# -68.518278 -15.443*1j,
# ])
#
# print ('test')
# print (points[0:-1])
# print (points[1:])
#
#
#
#
# distance,cap=deplacement(points[0:-1],points[1:])
# print ('resultat1')
# print (distance)
# print (cap)
#
#
# points=np.array([[
# -68.51666 -15.551*1j,
# -68.515375-15.5515*1j,
# -68.51408  -15.478*1j,
# -68.518278 -15.443*1j,
# ]])
#
# res=deplacement(points[0][0], points[0][1])
# print ('resultat2\n',res)
# res=deplacement(points[0][1], points[0][2])
# print ('resultat2\n',res)
#
#
# point1=points[0][0]
# point2=points[0][1]
#
# print ('point1',point1)
# print ('point2',point2)
#
# depl1=deplacement(point1, point2)
#
# difference=point2-point1
# ag=np.angle(difference, deg=True)
# print('ag',ag)
#
#
# print('depl1',depl1)