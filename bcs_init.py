import random

from Crypto.Util import number

import bcs_parameters as parameters
import bcs_file_ops as file_ops
import bcs_crypto as crypto


def generate_q(user_name):
	"""
	:return: the prime number

	generates a prime number of whatever size is specified in the parameters list
	"""

	q = str(number.getPrime(parameters.crypto_size))

	if not file_ops.write("users/" + user_name + "/q", q, "w+"):
		print(parameters.error_msg)
		exit()

	return q


def generate_r(user_name):
	"""
	:return: a random number of whatever size in bits is specified in the parameters file

	generate the "randomly chosen element r E {0,1}^160; assuming that this means a 160-bit integer
	"""

	r = str(random.getrandbits(parameters.crypto_size))

	if not file_ops.write("users/" + user_name + "/r", r, "w+"):
		print(parameters.error_msg)
		exit()

	return r


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
		print("Coefficient no. " + str(i) + " " + str(coefficient))
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


def initialize_instruction_table(user_name, polynomial, feature_count, pwd, r , q):
	"""
	:param user_name
	:param polynomial
	:param feature_count: number of features (i.e. the degree of the polynomial)
	:param pwd: the plain text password
	:param r

	basically:
	alpha = y0ai + G(pwd,a) * (2 * i) mod q
	beta = y1ai + G(pwd,a) * (2 * i + 1) mod q
	"""
	
	alpha = []
	beta = []

	for i in range(1, feature_count + 1):
		alpha_y = get_y(polynomial, 2 * i, feature_count)
		beta_y = get_y(polynomial, 2 * i + 1, feature_count)

		alpha.append(alpha_y + crypto.get_alpha_prf(pwd, r, i) % int(q))
		beta.append(beta_y + crypto.get_beta_prf(pwd, r, i) % int(q))

	instructions = ""

	for i in range(len(alpha)):
		instructions += str(alpha[i]) + " "
	instructions = instructions[:-1] + "\n"

	for i in range(len(beta)):
		instructions += str(beta[i]) + " "

	if not file_ops.write("users/" + user_name + "/instructions", instructions[:-1], "w"):
		print(parameters.error_msg)
		exit()

	print("\nInstruction table:\n" + str(instructions))