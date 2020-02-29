import os
import itertools
import random

from mpmath import *

import bcs_parameters as parameters
import bcs_history as history
import bcs_init as init
import statistics as stat
import bcs_crypto as crypto


def create_user_files(user_name):
	"""
	:param user_name: name of the user who is registering
	:return: 1 if all folders/files could be created, 0 otherwise

	create all the folders and files for a user during sign up
	"""

	if not os.path.exists(user_name):
		try:
			os.makedirs("users/" + user_name)

			f = open("users/" + user_name + "/history", "w+")
			f.close()

			f = open("users/" + user_name + "/instructions", "w+")
			f.close()
		except IOError:
			return 0

	return 1


def compare_list_items(items):
	"""
	:param items: a list
	:return: 1 if all items are equal, 0 otherwise

	"""

	for a, b in itertools.combinations(items, 2):
		if a != b:
			return 0
	return 1


def pad_something(something):
	"""
	:param something: string which should be padded
	:return: string including appended padding

	appends a padding to a given input to a fixed output size using zeros;
	in this case to guarantee the fixed file size of the history file
	"""

	padding = len(something) % 16

	if padding != 0:
		something = something + ((16 - padding) * '0')

	return something + ((parameters.history_size - len(something)) * '0')


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


def is_distinguishing(mean, sdev):
	return abs(mean - parameters.t) > parameters.k * sdev


def update_instruction_table(polynomial, coefficient_count, password, r, updated_history):
	alpha = []
	beta = []

	regrouped = history.regroup_features(updated_history)

	for i in coefficient_count:
		mean = stat.mean(regrouped[i])
		sdev = stat.stdev(regrouped[i])

		if is_distinguishing(mean, sdev):
			if mean <= parameters.t:
				alpha_y = init.get_y(polynomial, 2 * i, coefficient_count)
				beta_y = random.getrandbits(160)
			else:
				alpha_y = random.getrandbits(160)
				beta_y = init.get_y(polynomial, 2 * i + 1, coefficient_count)
		else:
			alpha_y = init.get_y(polynomial, 2 * i, coefficient_count)
			beta_y = init.get_y(polynomial, 2 * i + 1, coefficient_count)

		alpha.append(alpha_y + crypto.get_alpha_prf(password, r, i))
		beta.append(beta_y + crypto.get_beta_prf(password, r, i))

	instructions = ""

	for i in range(len(alpha)):
		instructions += str(alpha[i]) + " "
	instructions = instructions[:-1] + "\n"

	for i in range(len(beta)):
		instructions += str(beta[i]) + " "

	return instructions[:-1]





