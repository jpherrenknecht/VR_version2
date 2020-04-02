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
pts=(0.5, 1, 1)
print('a011', a[0, 1, 1])
print('a111', a[1, 1, 1])

print('resultat',fn(pts))
