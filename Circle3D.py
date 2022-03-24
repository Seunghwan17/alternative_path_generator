from operator import matmul
from Point3D import Point3D
from TMatrix3D import TMatrix3D
import math

class Circle3D:
    """__normal: the outward-pointing vector which is perpendicular to the plane of a circle C
       __center: center of C, 
       __radius: radius of C"""
    def __init__(self, normal: Point3D, center: Point3D, radius: float) -> None:
        self._normal = normal
        self._center = center
        self._radius = radius
        
    def __str__(self) -> str:
        return ('center:' + '(' + str(self._center.xCoord()) + ', ' + str(self._center.yCoord()) + ', ' + str(self._center.zCoord()) + ')' + '\n'
                'radius:' + str(self._radius) + '\n'
                'normal:' + '(' + str(self._normal.xCoord()) + ', ' + str(self._normal.yCoord()) + ', ' + str(self._normal.zCoord()) + ')')        
        
    def normal(self) -> Point3D:
        return self._normal
    
    def center(self) -> Point3D:
        return self._center
    
    def radius(self) -> float:
        return self._radius
    
    def samples(self, numPoints) -> list:
        """evaluate the points on this circle with uniformly increasing polar angle in CCW"""
        samplesOnCircle = []
        
        PI = 3.14159265358979323846
        stepAngle = 2.0*PI / numPoints
        magitudeOfTangent = self._radius*math.tan(stepAngle)
        normal = self._normal
        normal = normal.unitVector()
        
        startPoint = Point3D(0.0, 0.0,0.0)
        unitZVector = Point3D(0.0, 0.0, 1.0)
        minusUnitZVector = Point3D(0.0, 0.0, -1.0)
        if normal.equal(unitZVector):
            startPoint.set_point(self._radius, 0.0, 0.0)
        elif normal.equal(minusUnitZVector):
            startPoint.set_point(-self._radius, 0.0, 0.0)
        else:
            rotationMat = TMatrix3D()
            rotationMat.rotate(unitZVector, normal)
            # startPoint = matmul(rotationMat, Point3D(self._radius, 0.0, 0.0))
            tmpStartPt = Point3D(self._radius, 0.0, 0.0)
            startPoint = rotationMat * tmpStartPt
            
        startPoint = self._center + startPoint
        
        samplesOnCircle.append(startPoint)
        currPoint = startPoint
        for i in range(numPoints-1):
            tangent = normal.cross_product(currPoint - self._center)
            tangent.normalize()
            
            sector = (currPoint + (magitudeOfTangent*tangent)) - self._center
            sector.normalize()
            
            currPoint = self._center + (self._radius*sector)
            samplesOnCircle.append(currPoint)
        
        return samplesOnCircle
        
