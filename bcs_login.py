import os

import bcs_keyboard as kb
import bcs_parameters as parameters
import bcs_misc as misc
import bcs_file_ops as file_ops
import bcs_crypto as crypto
import bcs_history as history
import bcs_init as init


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
        with open("users/" + user_name + "/r", "r") as file:
            r = file.read()

        with open("users/" + user_name + "/q", "r") as file:
            q = int(file.read())

        with open("users/" + user_name + "/instructions", "r") as file:
            instructions = []
            instruction_table = file.read().split("\n")

            for i in instruction_table:
                instructions.append(i.split(" "))

            print("Instruction table before login: " + str(instructions))

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
                y_i = alpha - (crypto.get_alpha_prf(password, r, i) % q)
                points.append((x_i, y_i))
            elif i <= coefficient_count:
                beta = int(instructions[1][i - 1])
                x_i = 2 * i + 1
                y_i = beta - (crypto.get_beta_prf(password, r, i) % q)
                points.append((x_i, y_i))

        print("Points: " + str(points))

        hardened_password = misc.lagrange_interpolation(points)(0)
        print("\nThe recovered hpwd is: ", hardened_password)
        print("\nDecrypting history file with hpwd...")

        nonce, tag, cipher_text = file_ops.read("users/" + user_name + "/history", "rb")
        decrypted = crypto.aes_decrypt(cipher_text, nonce, tag, crypto.derive_key(str(hardened_password)))

        if decrypted is None:
            print("\nSorry, login failed due to wrong password or typing pattern.")
            return

        print("\nHistory decrypted:\n" + str(decrypted.decode()))

        """ create new polynomial such that c[0] = hpwd """
        polynomial = init.generate_polynomial(q, coefficient_count)

        """ check history content against known plain text """
        if str(decrypted).find("---- BEGIN HISTORY ----") != -1:
            print("\nHpwd was recovered correctly, since the history was decrypted successfully!")

            """ update history file """
            updated_history = history.update_history(decrypted, features)

            print("Updated history file: ")
            print(updated_history)
            os.remove("users/" + user_name + "/history")

            if not file_ops.write("users/" + user_name + "/history", crypto.aes_encrypt(str(history.assemble_history(updated_history)), crypto.derive_key(str(polynomial[0]))), "wb"):
                print(parameters.error_msg)
                return

            """ update r """
            os.remove("users/" + user_name + "/r")
            new_r = init.generate_r(user_name)

            """ update instruction table """
            instruction_table = misc.update_instruction_table(polynomial, coefficient_count, password, new_r, updated_history, q)
            print("\nInstruction table:\n" + str(instruction_table))

            os.remove("users/" + user_name + "/instructions")
            if not file_ops.write("users/" + user_name + "/instructions", instruction_table, "w"):
                print(parameters.error_msg)
                return
        else:
            print("\nOooops, the hpwd was not recovered correctly!")
