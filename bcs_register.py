import os
import random

import bcs_parameters as parameters
import bcs_keyboard as kb
import bcs_misc as misc
import bcs_crypto as crypto
import bcs_file_ops as file_ops
import bcs_history as history
import bcs_init as init


def register_new_user(demo):
	"""
	:return: 1 if signup was successful, 0 otherwise

	performs all actions necessary to sign up a new user:
	* various sanity checks
	* read the password from user input n times
	* generate r, polynomial, q, instruction table
	* encrypt the history file with hpwd
	"""

	if not os.path.exists('users'):
		os.makedirs('users')
	
	names = os.listdir('users')
	user_name = ""
	
	while user_name == "" or user_name in names:
		if user_name in names:
			user_name = str(raw_input("Name already in use. Please enter another one: "))
		else:
			user_name = str(raw_input("Please enter a name: "))

	if demo:
		passwords = ["test", "test", "test"]
		print("\nPasswords entered: " + str(passwords))
		features = history.add_control_strings("58 59 45 43 44 66 89\n58 59 45 43 44 66 89\n58 59 45 43 44 66 89\n")
		print("\nFeatures measured:\n " + str(features))

	else:
		user_input = kb.read_input(parameters.rounds)  # read the password n times from the user user_input
		passwords = user_input[1]
		print(passwords)
		features = history.add_control_strings(user_input[0])
		print(features)

	# Check if the passwords entered are all the same
	if misc.compare_list_items(passwords) != 1 or misc.create_user_files(user_name) != 1:
		print(parameters.error_msg)
		exit()

	# Create random r and save it to the file system
	r = str(random.getrandbits(parameters.r_size))
	print(str(r))

	if not file_ops.write("users/" + user_name + "/r", r, "w+"):
		print(parameters.error_msg)
		exit()

	# Number of feature values (len(pwd) * 2 - 1) -> each character and delays between them
	coefficient_count = len(passwords[0]) * 2 - 1
	print("coeff count: " + str(coefficient_count))

	# Create and save the user's q
	q = init.generate_q()
	print("q: " + str(q))

	if not file_ops.write("users/" + user_name + "/q", str(q), "w+"):
		print(parameters.error_msg)
		exit()

	# Create a random polynomial
	polynomial = init.initialize_polynomial(q, coefficient_count)

	# Create the initial instruction table
	instruction_table = init.initialize_instruction_table(polynomial, coefficient_count, passwords[0])
	print("\nInstruction table:\n" + str(instruction_table))
	instructions = ""

	for i in range(len(instruction_table[0])):
		instructions += str(instruction_table[0][i]) + " "
	instructions = instructions[:-1] + "\n"

	for i in range(len(instruction_table[0])):
		instructions += str(instruction_table[1][i]) + " "
	instructions = instructions[:-1]

	# write instruction table to file system
	if not file_ops.write("users/" + user_name + "/instructions", instructions[:-1], "w"):
		print(parameters.error_msg)
		exit()

	# Initialize history, and encrypt it with polynomial[0] which is the hpwd
	print("\nEncryption key: " + str(polynomial[0]))

	cipher_text = crypto.aes_encrypt(misc.pad_something(features), crypto.derive_key(str(polynomial[0])))

	if not file_ops.write("users/" + user_name + "/history", cipher_text, "wb"):
		print(parameters.error_msg)
		exit()
