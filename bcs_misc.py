import random

from Crypto.Util import number
from mpmath import *

import bcs_file_ops as file_ops
import bcs_parameters as parameters


def lagrange_interpolation(points):
	"""
	:param points: points needed for interpolation of the polynomial
	:return: the interpolated polynomial

	this function is based on based on https://gist.github.com/melpomene/2482930
	and was adapted for higher precision using the mpmath library. Otherwise the
	reconstructed hpwd' would not match the initial hpwd 100%.
	e.g. initial hpwd:  351595031431585176588492245018341790008407547664
	reconstructed hpwd: 351595031431585176588492245018341790008407490560
	"""

	def p(x):
		mp.dps = 100
		total = mpf(0)
		n = len(points)

		for i in range(n):
			xi, yi = points[i]

			def g(i, n):
				tot_mul = mpf(1)

				for j in range(n):
					if i == j:
						continue

					xj, yj = points[j]
					tot_mul = tot_mul * (x - xj) / float(xi - xj)

				return tot_mul

			total = total + yi * g(i, n)

		if ceil(total) - total < 0.5:
			return int(ceil(total))
		else:
			return int(floor(total))

	return p


def get_y(polynomial, x, coefficient_count):

	"""
	:param polynomial: the random polynomial
	:param x: the x we want to know the y of
	:param coefficient_count: degree of the polynomial
	:return: the y we want to know

	helper function to determine the y of a given f(x) of degree m
	"""

	y = 0

	for i in range(0, coefficient_count):
		y = y + polynomial[i] * (x ** i)
		#print("y = " + str(y))
	return y


def generate_polynomial(q, coefficient_count):
	"""
	:param q: the random prime number
	:param coefficient_count: the desired degree of the random polynomial
	:return: the polynomials coefficients
	"""

	coefficients = []

	for i in range(coefficient_count):
		coefficient = (random.getrandbits(parameters.crypto_size) % int(q))
		coefficients.append(coefficient)

	return coefficients


def generate_r(user_name):
	"""
	:return: a random number of whatever size in bits is specified in the parameters file

	generates the "randomly chosen element r E {0,1}^160; assuming that this means a 160-bit integer
	"""

	r = str(random.getrandbits(parameters.crypto_size))

	if not file_ops.write("users/" + user_name + "/r", r, "w+"):
		return False

	return r


def generate_q(user_name):
	"""
	:return: the prime number

	generates a (probable) prime number of size specified in the parameters list
	"""

	q = str(number.getPrime(parameters.crypto_size))

	if not file_ops.write("users/" + user_name + "/q", q, "w+"):
		return False

	return q