import os
import bcs_keyboard as kb
import bcs_parameters as parameters
import sha3
import bcs_misc as misc
import bcs_file_ops as file_ops
import bcs_crypto as crypto


def login_as_user(demo):
	"""
	:return: 1 if login was successful, 0 otherwise

	the login function calls all the functions necessary to complete a login. this includes:
	* performing sanity checks if a user even exists
	* reading the password from the user input
	* recreate the polynomial points from the instruction table
	* interpolate the polynomial using the points
	* decrypt the history file and check against a known plain text
	* update the history file accordingly and basically perform all the initial steps
	"""

	# check if user accounts are present
	if not os.path.exists('users'):
		print("Sorry, no accounts available. Please sign up first.")
		return

	user_names = os.listdir('users')

	if not user_names:
		print("Sorry, no accounts available. Please sign up first.")
		return

	# get username from input
	username = raw_input("Enter name: ")

	if username not in user_names:
		print("Sorry, no such account.")
		return
	else:
		with open("users/" + username + "/instructions", "r") as file:
			instruction_table = file.read().split("\n")

		instructions = []
		for i in instruction_table:
			instructions.append(i.split(" "))
		print("login inttable: " + str(instructions))

		print("Enter password: ")

		if demo:
			password = "test"
			features = [58, 59, 45, 43, 44, 66, 89]
			### read login file
			### password = password from the file
			### features = measured values from the file
		else:
			user_input = kb.read_input(1)  # user enters password once
			password = user_input[1][0]	 # this is the password
			features = user_input[0].split(" ")  # this are the measured feature values

		feature_count = len(password) * 2 - 1

		print("\nInstruction table before logging in: " + str(instruction_table))

		# check threshold and correct errors / anomalies
		i = 0

		for f in features:
			if not int(f) < int(parameters.k):
				features[i] = -9000	# debug value
			i += 1

		points = []
		#features = [58, 59, 45, 43, 44, 66, 89] # debug values
		print("\nRecovering hpwd...")

		for i in range(1, len(features)+1):
			if not features[i-1] is -9000:
				print(instructions[0][i-1])
				alpha = int(instructions[0][i - 1])
				x_i = 2 * i
				y_i = alpha - int(sha3.sha3_512(password.encode('utf-8')).hexdigest(), 16) * (2 * i)
				points.append((x_i, y_i))
			elif i <= feature_count:
				print(instructions[1][i - 1])
				beta = int(instructions[1][i - 1])
				x_i = 2 * i + 1
				y_i = beta - int(sha3.sha3_512(password.encode('utf-8')).hexdigest(), 16) * (2 * i + 1)
				points.append((x_i, y_i))
			i += 1

		interpolated = misc.lagrange_interpolation(points)

		hardened_password = interpolated(0)
		print("\nThe recovered hpwd is: ", hardened_password)

		cipher_text = file_ops.read("users/" + username + "/history", "rb")

		if cipher_text is False:
			print(parameters.error_msg)
			exit()

		print("\nDecrypting history with hpwd...")
		decrypted = crypto.aes_decrypt(cipher_text, crypto.derive_key(str(hardened_password)))

		print("\nHistory decrypted:\n" + decrypted)

		#### check against known plain text
