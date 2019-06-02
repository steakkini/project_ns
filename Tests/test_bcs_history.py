from unittest import TestCase
from bcs_history import *
from FeatureVector import *


class TestBcsHistory(TestCase):
	def test_parse_features_from_history(self):
		with open("history_plain.txt", "r") as f:
			history = f.read()

		expected = [[72, 80, 55], [64, 79, 62], [62, 63, 65]]
		result = parse_features_from_history(history)
		self.assertEqual(expected, result)

	def test_regroup_features(self):
		with open("history_plain.txt", "r") as f:
			features = parse_features_from_history(f.read())

		expected = [[72, 64, 62], [80, 79, 63], [55, 62, 65]]
		result = regroup_features(features)
		self.assertEqual(expected, result)

	def test_update_history(self):
		with open("history_plain.txt", "r") as f:
			history = f.read()

		vector = FeatureVector()
		vector.append_duration(100)
		vector.append_duration(200)
		vector.append_delay(1)  # first pause, this gets removed by FeatureVector.get_delays()
		vector.append_delay(300)
		vector.append_delay(15)  # last pause, this gets removed by FeatureVector.get_delays()

		expected = [[72, 80, 55], [64, 79, 62], [62, 63, 65], [100, 200, 300]]
		result = update_history(history, vector)
		self.assertEquals(expected, result)

	def test_add_control_string(self):
		result = add_control_strings("test")
		expected = "---- BEGIN HISTORY ----\n" + "test" + "---- END HISTORY ----"

		self.assertEqual(result, expected)

	def test_assemble_history(self):
		history = [[72, 80, 55], [64, 79, 62], [62, 63, 65]]

		result = assemble_history(history)
		expected = misc.pad_something(add_control_strings("72 80 55 64 79 62 62 63 65 "))

		self.assertEqual(result, expected)