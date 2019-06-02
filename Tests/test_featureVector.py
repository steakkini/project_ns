from unittest import TestCase
from FeatureVector import *


class TestFeatureVector(TestCase):
	def test_get_features(self):
		vector = FeatureVector()
		vector.append_duration(100)
		vector.append_delay(50)
		vector.append_duration(200)
		vector.append_delay(60)
		vector.append_delay(70)
		vector.append_duration(300)

		expected = "100 200 300 60"
		result = vector.get_features_string()

		self.assertEquals(expected, result)
