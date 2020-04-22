import random
import statistics as stat

import bcs_crypto as crypto
import bcs_file_ops as file_ops
import bcs_misc as misc
import bcs_parameters as parameters


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
		alpha_y = misc.get_y(polynomial, 2 * i, feature_count)
		beta_y = misc.get_y(polynomial, 2 * i + 1, feature_count)

		alpha.append(alpha_y + crypto.get_prf(pwd, r, 2 * i) % int(q))
		beta.append(beta_y + crypto.get_prf(pwd, r, 2 * i + 1) % int(q))

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


def update_instruction_table(polynomial, coefficient_count, password, r, updated_history, q):
	alpha = []
	beta = []
	q = int(q)

	regrouped = []

	for i in range(len(updated_history[0])):
		feature_measurements = []

		for j in range(len(updated_history)):
			feature_measurements.append(int(updated_history[j][i]))

		regrouped.append(feature_measurements)

	for i in range(1, coefficient_count + 1):
		mean = stat.mean(regrouped[i-1])
		std_dev = stat.stdev(regrouped[i-1])
		print("mean ", mean)
		print("std_dev ", std_dev)

		if (abs(mean - parameters.threshold) > parameters.k * std_dev) and len(updated_history) == parameters.h:
			if mean <= parameters.threshold:
				alpha_y = misc.get_y(polynomial, 2 * i, coefficient_count)
				beta_y = random.getrandbits(parameters.crypto_size)
				print(alpha_y)
				print(beta_y)

			else:
				alpha_y = random.getrandbits(parameters.crypto_size)
				print(alpha_y)
				beta_y = misc.get_y(polynomial, 2 * i + 1, coefficient_count)
				print(beta_y)

		else:
			alpha_y = misc.get_y(polynomial, 2 * i, coefficient_count)
			beta_y = misc.get_y(polynomial, 2 * i + 1, coefficient_count)

		alpha.append(alpha_y + crypto.get_prf(password, r, 2 * i) % q)
		beta.append(beta_y + crypto.get_prf(password, r, 2 * i + 1) % q)

	instructions = ""

	for i in range(len(alpha)):
		instructions += str(alpha[i]) + " "
	instructions = instructions[:-1] + "\n"

	for i in range(len(beta)):
		instructions += str(beta[i]) + " "

	return instructions[:-1]