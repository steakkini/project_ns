import os

#from pip._vendor.distlib.compat import raw_input

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

    # check if user accounts are present
    if not os.path.exists('users'):
        print("Sorry, no accounts available. Please sign up first.")
        return

    user_names = os.listdir('users')

    if not user_names:
        print("Sorry, no accounts available. Please sign up first.")
        return

    # get username from input
    user_name = input("Enter name: ")

    if user_name not in user_names:
        print("Sorry, no such account.")
        return
    else:
        with open("users/" + user_name + "/instructions", "r") as file:
            instruction_table = file.read().split("\n")

        instructions = []
        for i in instruction_table:
            instructions.append(i.split(" "))
        print("login inttable: " + str(instructions))

        print("Enter password: ")

        with open("users/" + user_name + "/r", "r") as file:
            r = file.read()

        if demo:
            iiii = 1
        else:
            user_input = kb.read_input(1)  # user enters password once
            password = user_input[1][0]  # this is the password
            features = user_input[0].split(" ")

            print("features are: ")  # + str(features))
            print(features)

        coefficient_count = len(password) * 2 - 1
        features = list(map(int, features))
        i = 0

        for f in features:
            if not int(f) < int(parameters.k):
                features[i] = -9000  # debug value
            i += 1

        points = []
        # features = [58, 59, 45, 43, 44, 66, 89] # debug values
        print("\nRecovering hpwd...")
        print("\nUsing r " + str(r))
        print(len(features))
        for i in range(1, len(features) + 1):
            if not features[i - 1] is -9000:
                alpha = int(instructions[0][i - 1])
                x_i = 2 * i
                y_i = alpha - crypto.get_alpha_prf(password, r, i)
                # y_i = alpha - crypto.get_alpha_prf(password, r, x_i)
                points.append((x_i, y_i))
            elif i <= coefficient_count:
                beta = int(instructions[1][i - 1])
                x_i = 2 * i + 1
                y_i = beta - crypto.get_beta_prf(password, r, i)
                # y_i = beta - crypto.get_beta_prf(password, r, x_i)
                points.append((x_i, y_i))
            i += 1

        print("points: " + str(points))

        interpolated = misc.lagrange_interpolation(points)
        print("interpolated " + str(interpolated(0)))

        hardened_password = interpolated(0)
        print("\nThe recovered hpwd is: ", hardened_password)

        cipher_text = file_ops.read("users/" + user_name + "/history", "rb")

        if cipher_text is False:
            print(parameters.error_msg)
            exit()

        print("\nDecrypting history with hpwd...")
        decrypted = crypto.aes_decrypt(cipher_text, crypto.derive_key(str(hardened_password)))

        print("\nHistory decrypted:\n" + decrypted)

        """ check history content against known plain text """
        if str(decrypted).find("---- BEGIN HISTORY ----") != -1:
            print("\nHpwd was recovered correctly, since the history was decrypted successfully!")

            """ update history file """
            updated_history = history.update_history(decrypted, features)
            os.remove("users/" + user_name + "/history")
            cipher_text = crypto.aes_encrypt(str(misc.pad_something(str(history.assemble_history(updated_history)))),
                                             crypto.derive_key(str(hardened_password)))

            if not file_ops.write("users/" + user_name + "/history", cipher_text, "wb"):
                print(parameters.error_msg)
                exit()

            """ update r """
            os.remove("users/" + user_name + "/r")
            new_r = init.generate_r(user_name)

            """ update """
            os.remove("users/" + user_name + "/q")
            new_q = init.generate_q(user_name)

            """ create new polynomial such that c[0] = hpwd """
            print("coefficient count " + str(coefficient_count))
            polynomial = init.initialize_polynomial(new_q, coefficient_count)
            polynomial[0] = long(hardened_password)

            """ update instruction table """
            instruction_table = misc.update_instruction_table(polynomial, coefficient_count, password, r,
                                                              updated_history)
            print("\nInstruction table:\n" + str(instruction_table))

            os.remove("users/" + user_name + "/instructions")
            if not file_ops.write("users/" + user_name + "/instructions", instruction_table, "w"):
                print(parameters.error_msg)
                exit()
        else:
            print("\nOooops, the hpwd was not recovered correctly, since the history could not be decrypted!")
