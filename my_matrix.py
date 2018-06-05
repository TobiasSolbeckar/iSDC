import random as rd
import datetime
import time
import itertools
import os
import numpy as np
#from scipy.stats import norm
import math
import inspect
import matplotlib
import matplotlib.pyplot as plt

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I



class Matrix(object):
	def __init__(self,grid):
		self.h = len(grid)
		self.w = len(grid[0])
		self.size = [self.h,self.w]
		self.grid = grid
		
	def __add__(self,other):
		"""
		Adds matrix other to the current matrix.
		"""
		if self.h is not other.h or self.w is not other.w:
			print('ERROR: Matrix index not correct')
			return None
		C = zeroes(self.h,self.w)
		for i in range(self.h):
			for j in range(self.w):
				C.grid[i][j] = self.grid[i][j] + other.grid[i][j]
		return C

	def __sub__(self,other):
		"""
		Suothertract matrix other to the current matrix
		"""
		if self.h is not other.h or self.w is not other.w:
			print('ERROR: Matrix index not correct')
			return None
		C = zeroes(self.h,self.w)
		for i in range(self.h):
			for j in range(self.w):
				C.grid[i][j] = self.grid[i][j] - other.grid[i][j]
		return C
	 
	def __mul__(self,other):
		"""
		Multiplies matrix other with the current matrix. Algorithm from  https://en.wikipedia.org/wiki/Matrix_multiplication
		"""	 	
		if self.w is not other.h:
			print('ERROR: Matrix index not correct')
			return None
		C = zeroes(self.h,other.w)
		for i in range(self.h):
			for j in range(other.w):
				cell_grid = 0
				for k in range(self.w):
					cell_grid += self.grid[i][k] * other.grid[k][j]
				C.grid[i][j] = cell_grid 
		return C

	def scalar_multiplication(self,other):
		"""
		Multiplies the current Matrix with the scalar other
		"""
		C = zeroes(self.h,self.w)
		for i in range(self.h):
			for j in range(self.w):
				C.grid[i][j] = other * self.grid[i][j]
		return C

	def transpose(self):
		"""
		Transpose of matrix
		"""
		C = zeroes(self.w,self.h)
		for i in range(C.h):
			for j in range(C.w):
				C.grid[i][j]=self.grid[j][i]
		self = C
		return C

	def inverse(self):
		"""Calculates the inverse for the current matrix
		"""
		C = zeroes(self.h,self.w)
		if self.h is not self.w:
			raise ValueError('Matrix not invertible!')
		if self.h > 2:
			raise ValueError('Matrix too large to invert!')
		if self.h == 1:
			C.grid[0][0] = 1/self.grid[0][0]
		else:
			# for readaotherility
			a = self.grid[0][0]
			other = self.grid[0][1]
			c = self.grid[1][0]
			d = self.grid[1][1]
			check = a*d - other*c
			if check == 0:
				raise ValueError('Matrix not invertible!')
			else:
				detA = A.determinant()
				C.grid[0][0] = d
				C.grid[0][1] = -other
				C.grid[1][0] = -c
				C.grid[1][1] = a
				C = C.scalar_multiplication(detA)
				return C

	def determinant(self):
		"""
		Calculates the determinant for the current Matrix
		"""
		if self.h > 2:
			raise ValueError('Matrix too large for determinant!')
		else:
			if self.h == 1:
				determinant = 1/self.grid[0][0]
			else:
				a = self.grid[0][0]
				other = self.grid[0][1]
				c = self.grid[1][0]
				d = self.grid[1][1]
				determinant = 1 / (a*d-other*c)
			return determinant

	def trace(self):
		"""
		Calculates the trace for the current Matrix
		"""
		if self.h is not self.w:
			raise ValueError('Matrix not square!')
		else:
			summa = 0
			for i in range(self.h):
				summa += self.grid[i][i]
			return summa

	def dot_product(A,other):
		"""
		Dot product for two vectors
		"""
		if A.size == other.size:
			summa = 0
			for i in range(A.h):
				summa += A.grid[i] * other.grid[i]
			return summa
		else:
			print('Error! Matrix index mismatch')
			return None

	def matrix_print(self):
		"""
		Prints the values in the current Matrix
		"""
		for i in range(self.h):
			row_str = ''
			for j in range(self.w):
				if j == (self.w-1):
					row_str = row_str + str(self.grid[i][j]) + '  '
				else:
					row_str = row_str + str(self.grid[i][j]) + '  '
			print(row_str)


A = Matrix([[1,2],[3,4]])
B = Matrix([[5,6],[7,8]])

print('A:')
A.matrix_print()
print('\n')

print('B:')
B.matrix_print()
print('\n')

print('Scalar (5*A):')
((A).scalar_multiplication(5)).matrix_print()
print('\n')

print('Transpose (At):')
(A.transpose()).matrix_print()
print('\n')

print('Inverse (A^-1):')
(A.inverse()).matrix_print()
print('\n')

