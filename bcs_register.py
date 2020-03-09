import os

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
            user_name = str(input("Name already in use. Please enter another one: "))
        else:
            user_name = str(input("Please enter a name: "))

    if demo:
        iiii = 1
    else:
        print("\nEnter password and press TAB afterwards.")
        user_input = kb.read_input(1)
        password = user_input[1][0]

    if len(password) == 0:
        print("\nNo password entered.")
        return

    features = history.add_control_strings(user_input[0])

    print("\nPassword entered: " + str(password))
    print("\nFeatures measured:\n" + str(features))

    try:
        os.makedirs("users/" + user_name)
    except IOError:
        print(parameters.error_msg)
        return

    """ Number of feature values (len(pwd) * 2 - 1) -> each character and delays between them """
    coefficient_count = len(password) * 2 - 1
    print("\nNumber of coefficients: " + str(coefficient_count))

    """ Create random r and q and save them to the file system """
    r = init.generate_r(user_name)
    q = init.generate_q(user_name)

   # r, q, polynomial = init.create_user(user_name, )

    """ Create a random polynomial """
    polynomial = init.generate_polynomial(q, coefficient_count)
    print("\nThe hardened password is: " + str(polynomial[0]))

    """ Create the initial instruction table """
    init.initialize_instruction_table(user_name, polynomial, coefficient_count, password, r, q)

    """ Try to encrypt the new history file with the new hpwd and save it """
    if not file_ops.write("users/" + user_name + "/history", crypto.aes_encrypt(misc.pad_something(features), crypto.derive_key(str(polynomial[0]))), "wb"):
        print(parameters.error_msg)
        exit()
