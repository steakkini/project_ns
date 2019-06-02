from Crypto.Util import number
import random
import sha3
import bcs_parameters as parameters


def generate_q():
	"""
	:return: the prime number

	generates a prime number of whatever size is specified in the parameters list
	"""

	return number.getPrime(parameters.q_size)


def generate_r():
	"""
	:return: a random number of whatever size in bits is specified in the parameters file

	generate the "randomly chosen element r E {0,1}^160; assuming that this means a 160-bit integer
	"""

	return random.getrandbits(parameters.r_size)
	

def initialize_polynomial(q, coefficient_count):
	"""
	:param q: the random prime number
	:param coefficient_count: the desired degree of the random polynomial
	:return: the polynomials coefficients
	"""

	coefficients = []

	for i in range(coefficient_count):
		coefficients.append(random.getrandbits(parameters.q_size) % q)

	return coefficients


def get_y(polynomial, x, m):
	"""
	:param polynomial: the random polynomial
	:param x: the x we want to know the y of
	:param m: degree of the polynomial
	:return: the y we want to know

	helper function to determine the y of a given f(x) of degree m
	"""

	y = 0

	for i in range(0, m):
		y = y + polynomial[i] * (x ** i)
	return y


def initialize_instruction_table(polynomial, feature_count, pwd):
	"""
	:param polynomial: the random polynomial
	:param feature_count: number of features (i.e. the degree of the polynomial)
	:param pwd: the plain text password
	:return: 2 lists containing alpha and beta values

	basically:
	alpha = y0ai + G(pwd,a) * (2 * i) mod q
	beta = y1ai + G(pwd,a) * (2 * i + 1) mod q
	"""
	
	alpha = []
	beta = []

	for i in range(1, feature_count + 1):

		alpha_y = get_y(polynomial, 2 * i, feature_count)
		beta_y = get_y(polynomial, 2 * i + 1, feature_count)

		alpha_prf = int(sha3.sha3_512(pwd.encode('utf-8')).hexdigest(), 16) * (2 * i)
		beta_prf = int(sha3.sha3_512(pwd.encode('utf-8')).hexdigest(), 16) * (2 * i + 1)

		alpha.append(alpha_y + alpha_prf)
		beta.append(beta_y + beta_prf)

	return alpha, beta
