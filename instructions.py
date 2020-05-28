import random
import statistics as stat

import crypto as crypto
import file_ops as file_ops
import parameters as parameters


def init_instruction_table(user_name, polynomial, m, pwd, r, q):
	"""
	:param user_name
	:param polynomial
	:param m: number of features (i.e. the degree of the polynomial)
	:param pwd: the plain text password
	:param r

	basically:
	alpha = y0ai + G(pwd,a) * (2 * i) mod q
	beta = y1ai + G(pwd,a) * (2 * i + 1) mod q
	"""

	alpha = []
	beta = []

	for i in range(1, m + 1):
		y0ai = get_y(polynomial, 2 * i, m)
		y1ai = get_y(polynomial, 2 * i + 1, m)

		alpha.append(y0ai + crypto.get_prf(pwd, r, 2 * i) % int(q))
		beta.append(y1ai + crypto.get_prf(pwd, r, 2 * i + 1) % int(q))

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


def update_instruction_table(polynomial, m, password, r, updated_history, q):
	alpha = []
	beta = []
	q = int(q)

	regrouped = []

	for i in range(len(updated_history[0])):
		feature_measurements = []

		for j in range(len(updated_history)):
			feature_measurements.append(int(updated_history[j][i]))

		regrouped.append(feature_measurements)

	for i in range(1, m + 1):
		mean = stat.mean(regrouped[i-1])
		std_dev = stat.stdev(regrouped[i-1])
		print("mean ", mean)
		print("std_dev ", std_dev)

		if (abs(mean - parameters.t) > parameters.k * std_dev) and len(updated_history) == parameters.h:
			if mean <= parameters.t:
				alpha_y = get_y(polynomial, 2 * i, m)
				beta_y = random.getrandbits(parameters.crypto_size)

			else:
				alpha_y = random.getrandbits(parameters.crypto_size)
				beta_y = get_y(polynomial, 2 * i + 1, m)

		else:
			alpha_y = get_y(polynomial, 2 * i, m)
			beta_y = get_y(polynomial, 2 * i + 1, m)

		alpha.append(alpha_y + crypto.get_prf(password, r, 2 * i) % q)
		beta.append(beta_y + crypto.get_prf(password, r, 2 * i + 1) % q)

	instructions = ""

	for i in range(len(alpha)):
		instructions += str(alpha[i]) + " "
	instructions = instructions[:-1] + "\n"

	for i in range(len(beta)):
		instructions += str(beta[i]) + " "

	return instructions[:-1]


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
	return y
