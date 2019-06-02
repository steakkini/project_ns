import os
import itertools
import bcs_parameters as parameters
from mpmath import *
import numpy


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

		for i in xrange(n):
			xi, yi = points[i]

			def g(i, n):
				tot_mul = mpf(1)

				for j in xrange(n):
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


def calc_distinguishing_features(features):
	"""
	:param features: the features

	distinguishing feature: 0 if mean(last h succ. logins) + k*stddev(last h succ. logins) < ti
	distinguishing feature: 1 if mean(last h succ. logins) + k*stddev(last h succ. logins) > ti
	ti -> fixed parameter of the system
	k -> fixed parameter of the system (e.g. 0,2); k element of R+
	h -> fixed parameter; h element of N
	"""

	# t = 100
	t = numpy.mean(numpy.mean(features))
	print(t)
	k = 0.3
	h = 8

	for f in features:
		if numpy.mean(f) + k * numpy.std(f) < t:
			print(f, 0)
		if numpy.mean(f) + k * numpy.std(f) > t:
			print(f, 1)
		if numpy.mean(f) + k * numpy.std(f) == t:
			print(f, "/")
