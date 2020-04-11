from scipy.interpolate import RegularGridInterpolator
import  numpy  as np

#definition des graduations sur les axes x y z
x=np.arange(3)
y=np.arange(3)
z=np.arange(3)


# x = np.linspace(0, 2, 3)
# y = np.linspace(0, 2, 3)
# z = np.linspace(0, 2, 3)

# matrice des valeurs
a=np.arange(27).reshape(3,3,3)
fn = RegularGridInterpolator((x, y, z), a)

print()

#pts = np.array([[0.5, 1, 1], [0.5, 1, 1]])
# marche sous forme liste ou tuple
pts=np.array([[0.5, 1, 1],[0.51,1,1]])

print('a011', a[0, 1, 1])
print('a111', a[1, 1, 1])

print('resultat',fn(pts))


A= np.array([[2,3],[4,5]])
print ('A',A)
b = np.array([[7.,7.,7.]]).T
# B=np.insert(A,0,b,axis=1)
# print ('B',B)


A=np.array([[2+3*1j,4+5*1j,5+4*1j]])


B = np.zeros((3,len(A)))

C=b
real=np.real (A)
imag=np.imag (A)
print ('A',A)

print ('real',real)
print ('imag',imag)
print ('b',b)

print ('len A',len(A[0]))



b=np.ones((  len(A[0]), 1  ))*10
d=np.concatenate((np.real (A),np.imag (A)),axis=0).T
e=np.concatenate((b,d),axis=1)



print()
print ('d\n',d)
print('e\n',e)