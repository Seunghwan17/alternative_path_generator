from Circle3D import Circle3D
from Point3D import Point3D

# center1 = Point3D(1.0, 0.0, 0.0)
center1 = Point3D(0.0, 0.0, 1.0)
radius1 = 10.0
# normal = Point3D(0.0, 0.0, 1.0)
normal = Point3D(1.0, 0.0, 0.0)
circle1 = Circle3D(normal, center1, radius1)

print(circle1)
samples = circle1.samples(5)
for pt in samples:
    print(str(pt.xCoord()) + ', ' + str(pt.yCoord()), ' ' + str(pt.zCoord()))
