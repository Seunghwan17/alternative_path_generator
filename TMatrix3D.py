from operator import matmul
from Matrix import Matrix
from Point3D import Point3D 
import math
import RelOperator

class TMatrix3D(Matrix):
	def __init__(self) -> None:
		super().__init__(dims=(4,4), fill = 0)
		super().make_identity()
  
	def __mul__(self, other) -> Point3D:
		if isinstance(other, Point3D):
			hPt = Matrix(dims=(4,1), fill = 0)
			hPt[0,0] = other.xCoord()
			hPt[1,0] = other.yCoord()
			hPt[2,0] = other.zCoord()
			hPt[3,0] = 1.0
			result = matmul(self, hPt)
			# result = self * hPt
			if RelOperator.POS(result[3,0]):
				for i in range(4):
					result[i,0] = result[i,0] / result[3,0]
		point = Point3D(result[0,0], result[1,0], result[2,0])
		return point

	def __rmul__(self, other):
		return self.__mul__(other)
  
	def rotateX(self, cosine: float, sine: float) -> None:
		fill = 0.0
		rows = 2
		cols = 2
		mapping = [[fill] * cols for i in range(rows)]
		mapping[0][0] =  cosine
		mapping[0][1] = -sine
		mapping[1][0] =  sine
		mapping[1][1] =  cosine
  
		cols = 4
		willBeChanged = [[fill] * cols for i in range(rows)]
		for i in range(rows):
			for j in range(cols):
				willBeChanged[i][j] = self._element[i+1][j]
    
		for i in range(1,rows+1):
			for j in range(cols):
				self._element[i][j] = mapping[i-1][0] * willBeChanged[0][j] + mapping[i-1][1] * willBeChanged[1][j]
    
	def rotateY(self, cosine: float, sine: float) -> None:
		fill = 0.0
		rows = 2
		cols = 2
		mapping = [[fill] * cols for i in range(rows)]
		mapping[0][0] =  cosine
		mapping[0][1] =  sine
		mapping[1][0] = -sine
		mapping[1][1] =  cosine
  
		cols = 4
		willBeChanged = [[fill] * cols for i in range(rows)]
		for i in range(rows):
			for j in range(cols):
				willBeChanged[i][j] = self._element[i*2][j]
    
		for i in range(0,rows+1,2):
			for j in range(cols):
				self._element[i][j] = mapping[i//2][0] * willBeChanged[0][j] + mapping[i//2][1] * willBeChanged[1][j]

	def rotateZ(self, theta: float) -> None:
		fill = 0.0
		rows = 2
		cols = 2
		mapping = [[fill] * cols for i in range(rows)]
		mapping[0][0] =  math.cos(theta)
		mapping[0][1] =  -math.sin(theta)
		mapping[1][0] =  math.sin(theta)
		mapping[1][1] =  math.cos(theta)
  
		cols = 4
		willBeChanged = [[fill] * cols for i in range(rows)]
		for i in range(rows):
			for j in range(cols):
				willBeChanged[i][j] = self._element[i][j]

		for i in range(rows):
			for j in range(cols):
				self._element[i][j] = mapping[i][0] * willBeChanged[0][j] + mapping[i][1] * willBeChanged[1][j]

	def rotateArbitraryAxis(self, axis: Point3D, theta: float) -> None:
		axisX = axis.xCoord()
		axisY = axis.yCoord()
		axisZ = axis.zCoord()
  
		cosOfAxisX = 0.0
		sinOfAxisX = 0.0
		cosOfAxisY = 0.0
		sinOfAxisY = 0.0
		degreeZ = theta

		if RelOperator.LT(axisZ, 0,0):
			axisX = -axisX
			axisY = -axisY
			axisZ = -axisZ
			degreeZ=-degreeZ
   
		if RelOperator.NE(axisX, 0.0) or RelOperator.NE(axisY, 0.0):
			distanceOnlyYZ=math.sqrt( axisY*axisY + axisZ*axisZ )
			distance=axis.norm()

			if RelOperator.EQ(distanceOnlyYZ, 0.0):
				cosOfAxisX = 1.0
				sinOfAxisY = 0.0
			else:
				cosOfAxisX=axisZ/distanceOnlyYZ
				sinOfAxisX=axisY/distanceOnlyYZ
    
			cosOfAxisY=distanceOnlyYZ/distance
			sinOfAxisY=-axisX/distance
		else:
			self.rotateZ(degreeZ)
			return

		self.rotateX(cosOfAxisX,  sinOfAxisX)
		self.rotateY(cosOfAxisY, sinOfAxisY)
		self.rotateZ(degreeZ)
		self.rotateY(cosOfAxisY, -sinOfAxisY)
		self.rotateX(cosOfAxisX, -sinOfAxisX)

	def rotate(self, fromVector: Point3D, toVector: Point3D) -> None:
		originPt = Point3D(0., 0., 0.)
		if fromVector.equal(originPt) or toVector.equal(originPt) or fromVector.equal(toVector):
			return

		unitFromVector = fromVector/fromVector.norm()
		unitToVector = toVector/toVector.norm()
		theta = math.acos(unitFromVector.dot_product(unitToVector))
		axis = unitFromVector.cross_product(unitToVector)
		PHI = math.atan(1.0)*4.0
  
		if RelOperator.EQ(theta, 0.0):
			return
		elif RelOperator.EQ(theta,PHI):
			return
		else:
			self.rotateArbitraryAxis(axis, theta)