import os

import bcs_crypto as crypto
import bcs_file_ops as file_ops
import bcs_history as history
import bcs_instructions
import bcs_keyboard as kb
import bcs_misc
import bcs_misc as misc
import bcs_parameters as parameters


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

    everything_fine = True

    if not os.path.exists('users'):
        print("Sorry, no accounts available. Please sign up first.")
        return

    user_names = os.listdir('users')

    if not user_names:
        print("Sorry, no accounts available. Please sign up first.")
        return

    user_name = input("Enter name: ")

    if user_name not in user_names:
        print("Sorry, no such account.")
        return

    else:
        r = int(file_ops.read("users/" + user_name + "/r", "r"))
        if not r:
            print("\nNo r file available.")
            return

        q = int(file_ops.read("users/" + user_name + "/q", "r"))
        if not q:
            print("\nNo q file available.")
            return

        instruction_table = file_ops.read("users/" + user_name + "/instructions", "r")
        if not instruction_table:
            print("\nNo instruction table file available.")
            return

        instructions = []
        instruction_table = instruction_table.split("\n")

        for i in instruction_table:
            instructions.append(i.split(" "))

        if demo:
            iiii = 1
        else:
            print("Enter password: ")
            user_input = kb.read_input(1)
            password = user_input[1][0]

            if len(password) == 0:
                print("No password entered.")
                return

            features = list(map(int, (user_input[0].split(" "))))
            print("Features of current login: " + str(features))
            coefficient_count = len(password) * 2 - 1

        if len(instructions[0]) != coefficient_count:
            print("Password length does not match instruction table!")
            return

        error_correction = list(map(lambda x: x < parameters.threshold, features))
        points = []

        for i in range(1, len(features) + 1):
            if list(error_correction)[i-1]:
                alpha = int(instructions[0][i - 1])
                x_i = 2 * i
                y_i = alpha - (crypto.get_prf(password, str(r), 2 * i) % q)
                points.append((x_i, y_i))
            elif i <= coefficient_count:
                beta = int(instructions[1][i - 1])
                x_i = 2 * i + 1
                y_i = beta - (crypto.get_prf(password, str(r), 2 * i + 1) % q)
                points.append((x_i, y_i))

        print("Points: " + str(points))

        hardened_password = misc.lagrange_interpolation(points)(0)
        print("\nThe reconstructed hpwd is: ", hardened_password)
        print("\nTrying to decrypt history file with hpwd...")

        nonce, tag, cipher_text = file_ops.read("users/" + user_name + "/history", "rb")
        if not nonce or not tag or not cipher_text:
            print("\nNo history file available.")
            return

        decrypted = crypto.aes_decrypt(cipher_text, nonce, tag, crypto.derive_key(hardened_password).digest())

        if decrypted is None:
            print("\nLogin failed due to wrong password or typing pattern.")
            print("\nHpwd was not recovered correctly!")
            print('           ."`".'     )
            print("       .-./ _=_ \.-." )
            print("      {  (,(oYo),) }}")
            print('      {{ |   "   |} }')
            print("      { { \(---)/  }}")
            print("      {{  }'-=-'{ } }")
            print("      { { }._:_.{  }}")
            print("      {{  } -:- { } }")
            print("      {_{ }`===`{  _}")
            print("     ((((\)     (/))))")
            print("\nYou won't get in here >:D")

            return

        """ create new polynomial such that c[0] = hpwd """
        polynomial = bcs_misc.generate_polynomial(q, coefficient_count)

        print("\nHpwd was recovered correctly, since the history was decrypted successfully!")

        """ update history file """
        updated_history = history.update_history(decrypted, features)

        print("Updated history file: ")
        print(updated_history)
        os.remove("users/" + user_name + "/history")

        if not file_ops.write("users/" + user_name + "/history", crypto.aes_encrypt(str(history.assemble_history(updated_history)), crypto.derive_key(polynomial[0]).digest()), "wb"):
            print(parameters.error_msg)
            return

        """ update r """
        os.remove("users/" + user_name + "/r")
        new_r = bcs_misc.generate_r(user_name)

        """ update instruction table """
        instruction_table = bcs_instructions.update_instruction_table(polynomial, coefficient_count, password, new_r, updated_history, q)
        print("\nInstruction table:\n" + str(instruction_table))

        os.remove("users/" + user_name + "/instructions")
        if not file_ops.write("users/" + user_name + "/instructions", instruction_table, "w"):
            print(parameters.error_msg)
            return
