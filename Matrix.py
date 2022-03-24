from operator import matmul

class Matrix:
	def __init__(self, dims, fill) -> None:
		self._rows = dims[0]
		self._cols = dims[1]
		self._element = [[fill] * self._cols for i in range(self._rows)]
  
	def make_identity(self) -> None:
		if self._rows != self._cols:
			return
		for i in range(self._rows):
			for j in range(self._cols):
				if i == j:
					self._element[i][j] = 1.0
				else:
					self._element[i][j] = 0.0
		
	def __str__(self) -> str:
		m = len(self._element)
		matrixStr = ''
		for i in range(m):
			matrixStr += ('|' + ', '.join( map(lambda x:'{0:8.3f}'.format(x), self._element[i])) + '| \n')
		return matrixStr
 
	def __add__(self, other):
		result = Matrix( dims = (self._rows, self._cols), fill = 0)
		
		if isinstance (other, Matrix):
			for i in range(self._rows):
				for j in range(self._cols):
					result._element[i][j] = self._element[i][j] + other._element[i][j]
		elif isinstance (other, (int, float)):
			for i in range(self._rows):
				for j in range(self._cols):
					result._element[i][j] = self._element[i][j] + other
		return result
	
	def __radd__(self, other):
		return self.__add__(other)
	
	def __mul__(self, other):
		result = Matrix( dims = (self._rows, self._cols), fill = 0)
		if isinstance(other, Matrix):
			for i in range(self._rows):
				for j in range(self._cols):
					result._element[i][j] = self._element[i][j] * other._element[i][j]
		elif isinstance(other, (int, float)):
			for i in range(self._rows):
				for j in range(self._cols):
					result._element[i][j] = self._element[i][j] * other
					
		return result 
	
	def __rmul__(self, other):
		return self.__mul__(other)

	def __matmul__(self, other):
		result = Matrix( dims = (self._rows, other._cols), fill = 0)
		if isinstance(other, Matrix) and (self._cols == other._rows):
			for i in range(self._rows):
				for j in range(other._cols):
					accumulation = 0
					for k in range(self._cols):
						accumulation += self._element[i][k] * other._element[k][j]
					result._element[i][j] = accumulation
		return result

	def __getitem__(self, key):
		if isinstance(key, tuple):
			i = key[0]
			j = key[1]
			return self._element[i][j]

	def __setitem__(self, key, value):
		if isinstance(key, tuple):
			i = key[0]
			j = key[1]
			self._element[i][j] = value
	
if __name__=='__main__':
	A = Matrix(dims=(3,3), fill = 1)
	B = Matrix(dims=(3,3), fill = 2)
	C = 10*A
	D = A+B
	E = matmul(A,B)
	F = A*B
	# A[0,1] = 2
	# print(A[0,1])
	print(A)
	print(B)
	print(C)
	print(D)
	print(E)