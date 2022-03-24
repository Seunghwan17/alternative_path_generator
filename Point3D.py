import math
import RelOperator

class Point3D:
    def __init__(self, xCoord: float, yCoord: float, zCoord: float) -> None:
        self._xCoord = xCoord
        self._yCoord = yCoord
        self._zCoord = zCoord
        
    def __str__(self) -> str:
        return ('x:' + str(self._xCoord) + ', y:' + str(self._yCoord) + ', z:' + str(self._zCoord))
        
    def xCoord(self) -> float:
        return self._xCoord
        
    def yCoord(self) -> float:
        return self._yCoord
    
    def zCoord(self) -> float:
        return self._zCoord
    
    def norm(self) -> float:
        return math.sqrt(self._xCoord*self._xCoord + self._yCoord*self._yCoord + self._zCoord*self._zCoord)
    
    def unitVector(self):
        return Point3D(self._xCoord/self.norm(), self._yCoord/self.norm(), self._zCoord/self.norm())
    
    def normalize(self):
        norm = self.norm()
        self._xCoord = self._xCoord/norm
        self._yCoord = self._yCoord/norm
        self._zCoord = self._zCoord/norm
        
    def set_point(self, xCoord: float, yCoord: float, zCoord: float) -> None:
        self._xCoord = xCoord
        self._yCoord = yCoord
        self._zCoord = zCoord
    
    def equal(self, point) -> bool:
        if RelOperator.EQ(self._xCoord, point._xCoord) and RelOperator.EQ(self._yCoord, point._yCoord) and RelOperator.EQ(self._zCoord, point._zCoord):
            return True
        else:
            return False
                
    def distance(self, point) -> float:
        diffX = (self._xCoord - point._xCoord)
        diffY = (self._yCoord - point._yCoord)
        diffZ = (self._zCoord - point._zCoord)
        return math.sqrt(diffX*diffX + diffY*diffY + diffZ*diffZ)
    
    def __sub__(self, point):
        diffX = (self._xCoord - point._xCoord)
        diffY = (self._yCoord - point._yCoord)
        diffZ = (self._zCoord - point._zCoord)
        return Point3D(diffX, diffY, diffZ)
    
    def __rsub__(self, point):
        return self.__sub__(point)
    
    def __add__(self, point):
        addX = (self._xCoord + point._xCoord)
        addY = (self._yCoord + point._yCoord)
        addZ = (self._zCoord + point._zCoord)
        return Point3D(addX, addY, addZ)
    
    def __radd__(self, point):
        return self.__add__(point)
    
    def __mul__(self, other):
        result = Point3D(0.0, 0.0, 0.0)
        if isinstance(other, (int, float)):
            result.set_point(self._xCoord*other, self._yCoord*other, self._zCoord*other)
        return result
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        result = Point3D(0.0, 0.0, 0.0)
        if isinstance(other, (int, float)):
            result.set_point(self._xCoord/other, self._yCoord/other, self._zCoord/other)
        return result
    
    def __rtruediv__(self, other):
        return self.__truediv__(other)
    
    def dot_product(self, point) -> float:
        return (self._xCoord*point._xCoord + self._yCoord*point._yCoord + self._zCoord*point._zCoord)
    
    def cross_product(self, point):
        result = Point3D(self._yCoord*point._zCoord-self._zCoord*point._yCoord, self._zCoord*point._xCoord-self._xCoord*point._zCoord, self._xCoord*point._yCoord-self._yCoord*point._xCoord)
        return result
    
        
        