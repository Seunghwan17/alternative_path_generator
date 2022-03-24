from Circle3D import Circle3D
from Point3D import Point3D
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


2199030.097130068	-5971594.017483919	-2022051.8887581518
2195343.132152325	-5872813.2445228435	-2005066.7305489234
# center1 = Point3D(1.0, 0.0, 0.0)
center1 = Point3D(2195343.132152325, -5872813.2445228435, -2005066.7305489234)
radius1 = 100000.0
# normal = Point3D(0.0, 0.0, 1.0)
normal = Point3D(2195343.132152325 - 2199030.097130068, -5872813.2445228435 + 5971594.017483919, -2005066.7305489234 + 2022051.8887581518)
normal.normalize()
circle1 = Circle3D(normal, center1, radius1)

print(circle1)
xs = []
ys = []
zs = []
samples = circle1.samples(5)
for pt in samples:
    print(str(pt.xCoord()) + ', ' + str(pt.yCoord()), ' ' + str(pt.zCoord()))
    xs.append(
        pt.xCoord()  
    )
    ys.append(
        pt.yCoord()  
    )
    zs.append(
        pt.zCoord()  
    )


fig = plt.figure(figsize=(16, 16))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xs, ys, zs, color="blue", marker='o', s=15, cmap='Greens')
plt.savefig('abc.png')