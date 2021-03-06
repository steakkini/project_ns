import os

import crypto as crypto
import file_ops as file_ops
import history as history
import instructions as inttable
import keyboard as kb
import misc as misc
import parameters as parameters


def login_as_user(demo, d_uname, d_password, d_features):
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
        return False

    user_names = os.listdir('users')

    if not user_names:
        print("Sorry, no accounts available. Please sign up first.")
        return False

    if demo:
        user_name = d_uname
    else:
        user_name = input("Enter name: ")

    if user_name not in user_names:
        print("Sorry, no such account.")
        return False

    else:
        r = int(file_ops.read("users/" + user_name + "/r", "r"))
        if not r:
            print("\nNo r file available.")
            return False

        q = int(file_ops.read("users/" + user_name + "/q", "r"))
        if not q:
            print("\nNo q file available.")
            return False

        instruction_table = file_ops.read("users/" + user_name + "/instructions", "r")
        if not instruction_table:
            print("\nNo instruction table file available.")
            return False

        instructions = []
        instruction_table = instruction_table.split("\n")

        for i in instruction_table:
            instructions.append(i.split(" "))

        if demo:
            password = d_password
            features = d_features
            print("Features of current login: ", features)

        else:
            print("Enter password: ")
            user_input = kb.read_input(1)
            password = user_input[1][0]

            if len(password) == 0:
                print("No password entered.")
                return False

            features = list(map(int, (user_input[0].split(" "))))
            print("Features of current login: ", features)

        m = len(password) * 2 - 1

        if len(instructions[0]) != m:
            print("Password length does not match instruction table!")
            return False

        feature_below_t = list(map(lambda feature: feature < parameters.t, features))
        points = []

        for i in range(1, len(features) + 1):
            if list(feature_below_t)[i-1]:
                alpha = int(instructions[0][i - 1])
                x_i = 2 * i
                y_i = alpha - (crypto.get_prf(password, str(r), 2 * i) % q)
                points.append((x_i, y_i))
            #elif i <= m:
            else:
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
            return False

        decrypted = crypto.aes_decrypt(cipher_text, nonce, tag, crypto.get_aes_key(hardened_password).digest())

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

            return False

        """ create new polynomial such that c[0] = hpwd """
        polynomial = misc.generate_polynomial(q, m)

        print("\nHpwd was recovered correctly, since the history was decrypted successfully!")

        """ update history file """
        updated_history = history.update_history(decrypted, features)

        print("Updated history file: ")
        print(updated_history)
        os.remove("users/" + user_name + "/history")

        if not file_ops.write("users/" + user_name + "/history", crypto.aes_encrypt(str(history.assemble_history(updated_history)), crypto.get_aes_key(polynomial[0]).digest()), "wb"):
            print(parameters.error_msg)
            return False

        """ update r """
        os.remove("users/" + user_name + "/r")
        new_r = misc.generate_r(user_name)

        """ update instruction table """
        instruction_table = inttable.update_instruction_table(polynomial, m, password, new_r, updated_history, q)
        print("\nInstruction table:\n" + str(instruction_table))

        os.remove("users/" + user_name + "/instructions")
        if not file_ops.write("users/" + user_name + "/instructions", instruction_table, "w"):
            print(parameters.error_msg)
            return False

        return True
