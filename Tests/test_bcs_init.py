from unittest import TestCase
import bcs_init as init
import bcs_parameters as parameters


class TestBcsInit(TestCase):
	# def test_initialize_user_hpwd(self):

	# def test_generate_r(self):

	def test_initialize_polynomial(self):
		# param: q, coefficient_count

		result = init.initialize_polynomial(parameters.q, 5)
		print (result)

	# def initialize_instruction_table(q, feature_count, pwd):
