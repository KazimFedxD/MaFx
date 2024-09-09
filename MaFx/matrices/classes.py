from __future__ import annotations
from typing import Optional

class Matrix:
    def __init__(self, rows: int, cols: int, data: Optional[list[list[int]]] = None):
        """
        Initialize a new Matrix object with the given number of rows and columns.
        If data is provided, it should be a list of lists containing the matrix elements.
        """
        self.rows = rows
        self.cols = cols
        self.setdata(data or [[0] * cols for _ in range(rows)])

    @property
    def square(self) -> bool:
        return self.rows == self.cols
    
    @property
    def symmetric(self) -> bool:
        return self == self.transpose()
    
    @property
    def skew_symmetric(self) -> bool:
        return self == self.transpose() * -1
    
    @property
    def diagonal(self) -> bool:
        return all(self.data[i][j] == 0 for i in range(self.rows) for j in range(self.cols) if i != j)
    
    @property
    def scalar(self) -> bool:
        return self.diagonal and self.data[0][0] == self.data[1][1] == self.data[2][2]
    
    @property
    def trace(self) -> int:
        if not self.square:
            raise ValueError("Matrix must be square")
        return sum(self.data[i][i] for i in range(self.rows))
    
    @property
    def upper_triangular(self) -> bool:
        return all(self.data[i][j] == 0 for i in range(self.rows) for j in range(self.cols) if i > j)
    
    @property
    def lower_triangular(self) -> bool:
        return all(self.data[i][j] == 0 for i in range(self.rows) for j in range(self.cols) if i < j)
    
    @property
    def orthogonal(self) -> bool:
        return self * self.transpose() == Matrix.identity(self.rows)
    
    @property
    def nepotent_index(self) -> int:
        if not self.square:
            raise ValueError("Matrix must be square")
        i = 1
        while True:
            if self ** i == Matrix.zeros(self.rows, self.cols):
                return i
            i += 1
        
    @property
    def nilpotent(self) -> bool:
        return self.nepotent_index < float("inf")
    
    @property
    def rank(self) -> int:
        return len(self.rref())
    
    @property
    def rref(self) -> Matrix:
        matrix = self.copy()
        lead = 0
        for r in range(matrix.rows):
            if lead >= matrix.cols:
                return matrix
            i = r
            while matrix.data[i][lead] == 0:
                i += 1
                if i == matrix.rows:
                    i = r
                    lead += 1
                    if matrix.cols == lead:
                        return matrix
            matrix.data[i], matrix.data[r] = matrix.data[r], matrix.data[i]
            lv = matrix.data[r][lead]
            matrix.data[r] = [mrx / float(lv) for mrx in matrix.data[r]]
            for i in range(matrix.rows):
                if i != r:
                    lv = matrix.data[i][lead]
                    matrix.data[i] = [iv - lv*rv for rv, iv in zip(matrix.data[r], matrix.data[i])]
            lead += 1
        return matrix
    
    def copy(self) -> Matrix:
        return Matrix(self.rows, self.cols, self.data)
    
    def set(self, row: int, col: int, val: int) -> None:
        self.data[row][col] = val
        
    def get(self, row: int, col: int) -> int:
        return self.data[row][col]
    
    def getrow(self, row: int) -> list[int]:
        return self.data[row]
    
    def getcol(self, col: int) -> list[int]:
        return [row[col] for row in self.data]
    

    def setdata(self, data: list[list[int]]) -> None:
        if len(data) != self.rows or any(len(row) != self.cols for row in data):
            raise ValueError("Invalid data dimensions")
        self.data = data
    
    def inverse(self) -> Matrix:
        if self.rows != self.cols:
            raise ValueError("Matrix must be square")
        determinant = self.determinant()
        if determinant == 0:
            raise ValueError("Matrix is not invertible")
        
        adjugate = self.adjugate()
        return adjugate / determinant
    
           
    def determinant(self) -> int:
        if self.rows != self.cols:
            raise ValueError("Matrix must be square")
        if self.rows == 1:
            return self.data[0][0]
        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        det = 0
        for i in range(self.cols):
            det += ((-1) ** i) * self.data[0][i] * self.minor(0, i).determinant()
        return det
    
    def minor(self, row: int, col: int) -> Matrix:
        if self.rows < 2 or self.cols < 2:
            raise ValueError("Matrix is too small")
        data = [[self.data[i][j] for j in range(self.cols) if j != col] for i in range(self.rows) if i != row]
        return Matrix(self.rows - 1, self.cols - 1, data)
    
    def cofactor(self) -> Matrix:
        data = [[((-1) ** (i + j)) * self.minor(i, j).determinant() for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(self.rows, self.cols, data)
    
    def adjugate(self) -> Matrix:
        return self.cofactor().transpose()
    
    def transpose(self) -> Matrix:
        data = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(self.cols, self.rows, data)
    
    def __repr__(self):
        return f"Matrix({self.rows}, {self.cols}, {self.data})"
    
    
    def __str__(self):
        string = ""
        for row in self.data:
            for val in row:
                string += f"{val} "
            string += "\n"
        return string
    
    def __eq__(self, other: Matrix) -> bool:
        return self.data == other.data
    
    def __add__(self, other: Matrix) -> Matrix:
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions")
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] + other.data[i][j]
        return result
    
    def __sub__(self, other: Matrix) -> Matrix:
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions")
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] - other.data[i][j]
        return result
    

    def __mul__(self, other: Matrix|int|float) -> Matrix:
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError("Invalid matrix dimensions")
            result = Matrix(self.rows, other.cols)
            for i in range(self.rows):
                for j in range(other.cols):
                    for k in range(self.cols):
                        result.data[i][j] += self.data[i][k] * other.data[k][j]
            return result
    
        elif isinstance(other, (int, float)):
            result = Matrix(self.rows, self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    result.data[i][j] = self.data[i][j] * other
            return result
        else:
            raise TypeError("Invalid type for multiplication")
    
    def __rmul__(self, other: Matrix|int|float) -> Matrix:
        return self * other
    
    def __truediv__(self, other: Matrix|int|float) -> Matrix:
        if isinstance(other, (int, float)):
            result = Matrix(self.rows, self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    result.data[i][j] = self.data[i][j] / other
            return result
        elif isinstance(other, Matrix):
            result = self * other.inverse()
            return result
        else:
            raise TypeError("Invalid type for division")
        
    def __pow__(self, power: int) -> Matrix:
        if power < 0:
            raise ValueError("Invalid power")
        if power == 0:
            return Matrix.identity(self.rows)
        result = self
        for _ in range(power - 1):
            result = result * self
        return result
    
    @staticmethod
    def identity(n: int) -> Matrix:
        data = [[0] * n for _ in range(n)]
        for i in range(n):
            data[i][i] = 1
        return Matrix(n, n, data)
    
    @staticmethod
    def zeros(rows: int, cols: int) -> Matrix:
        return Matrix(rows, cols)
    
    @staticmethod
    def ones(rows: int, cols: int) -> Matrix:
        data = [[1] * cols for _ in range(rows)]
        return Matrix(rows, cols, data)
    
    @staticmethod
    def random(rows: int, cols: int) -> Matrix:
        from random import randint
        data = [[randint(0, 9) for _ in range(cols)] for _ in range(rows)]
        return Matrix(rows, cols, data)
    
    @staticmethod
    def from_list(data: list[list[int]]) -> Matrix:
        rows = len(data)
        cols = len(data[0])
        return Matrix(rows, cols, data)
    
    @staticmethod
    def from_string(string: str) -> Matrix:
        data = [[int(val) for val in row.split()] for row in string.split("\n")]
        return Matrix(len(data), len(data[0]), data)
    
    @staticmethod
    def from_file(filename: str) -> Matrix:
        with open(filename, "r") as file:
            return Matrix.from_string(file.read())
    
    def to_list(self) -> list[list[int]]:
        return self.data
    
    def to_file(self, filename: str) -> None:
        with open(filename, "w") as file:
            file.write(str(self))
            
    def to_string(self) -> str:
        return str(self)
    
    def to_latex(self) -> str:
        string = "\\begin{bmatrix}\n"
        for row in self.data:
            string += " & ".join(str(val) for val in row)
            string += "\\\\\n"
        string += "\\end{bmatrix}"
        return string
    
    
        
            


a = Matrix(3, 2, [[1, 2], [1, 4], [1, 4]])

