import bcs_parameters as parameters
import bcs_misc as misc


def parse_features_from_history(history):
	"""
	:param history: the history string including control strings (e.g. ---- BEGIN HISTORY ----)
	:return: a list of feature measurements

	parses the history text into a list containing lists of feature measurements
	"""

	feature_start = parameters.pos  # directly after "---- BEGIN HISTORY ----\n"
	feature_end = history.find("\n---- END HISTORY ----")  # directly before "\n---- END HISTORY ----"

	if "---- BEGIN HISTORY ----" not in history:
		return "history damaged."

	features = history[feature_start:feature_end]
	result = []

	for line in features.splitlines():
		result.append([int(i) for i in line.split(" ")])

	return result


def regroup_features(features):
	"""
	:param features: a list of features
	:return: basically the same list but structured differently (see below)

	regroups distinct measurements of the same feature into lists
	as preparation for standard dev and mean calculation, like so:
	f1, f2, f3, f4
	f1, f2, f3, f4
	becomes
	f1, f1
	f2, f2
	...
	"""

	regrouped = []

	for i in range(len(features[0])):
		feature_measurements = []

		for j in range(len(features)):
			feature_measurements.append(int(features[j][i]))

		regrouped.append(feature_measurements)

	return regrouped


def update_history(current_history, feature_vector):
	"""
	:param current_history: current, plain text history
	:param feature_vector: updated, plain text history
	:return: the updated, plain text history

	updates the history file accordingly upon a successful login. the number of logins kept in the history file
	depends on the value assigned to parameters.h in the parameters list.
	"""

	current_history = parse_features_from_history(current_history)

	if len(current_history) > parameters.h:
		current_history = current_history[-1:]

	current_history.append(feature_vector.get_features_list())

	return current_history


def add_control_strings(history):
	"""
	:param history:
	:return: the history string including pre/appended control strings

	pre/appends the control string to make sure that the decryption went fine, meaning that a) the provided
	password is correct and also the biometrical features match those from previous logins
	"""

	return "---- BEGIN HISTORY ----\n" + ''.join(history) + "---- END HISTORY ----"


def assemble_history(history):
	"""
	:param history: list of feature measurements
	:return: the history string including pre/appended control strings and padding

	takes the nested list containing the feature measurement, converts everything into a string,
	pre/appends the control string and finally pads the history with 0s.
	"""

	history_string = ""
	for i in history:
		for j in i:
			history_string += str(j) + " "

	return misc.pad_something(add_control_strings(history_string))

