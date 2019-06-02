from unittest import TestCase
import bcs_misc as misc
import os
import shutil


class TestBcsMisc(TestCase):
	def test_create_user_files(self):
		os.chdir('..')

		result = misc.create_user_files(user_name="absdfk")
		history_file = os.path.exists("users/absdfk/history")
		instruction_file = os.path.exists("users/absdfk/instructions")

		self.assertEqual(result, 1)
		self.assertEqual(history_file, True)
		self.assertEqual(instruction_file, True)

		shutil.rmtree("users/absdfk")

	def test_compare_list_items(self):
		l1 = [['t', 'e', 's', 't'], ['t', 'e', 's', 't']]
		l2 = [['t', 's', 's', 't'],  ['t', 'e', 's', 't']]

		self.assertEqual(misc.compare_list_items(l1), 1)
		self.assertEqual(misc.compare_list_items(l2), 0)

	def test_pad_something(self):
		padded_1 = misc.pad_something("holy shizzleeee!")
		padded_2 = misc.pad_something(" ")

		self.assertEqual(len(padded_1), len(padded_2))



