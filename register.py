import os

import crypto as crypto
import file_ops as file_ops
import history
import instructions as inttable
import keyboard as kb
import misc
import parameters as parameters


def register_new_user(demo, d_uname, d_password, d_features):
    """
	:return: 1 if signup was successful, 0 otherwise

	performs all actions necessary to sign up a new user:
	* various sanity checks
	* read the password from user input n times
	* generate r, polynomial, q, instruction table
	* encrypt the history file with hpwd
	"""

    everything_fine = True

    if not os.path.exists('users'):
        os.makedirs('users')

    names = os.listdir('users')
    user_name = ""

    if demo:
        user_name = d_uname
        password = d_password
        features = ""
        for f in d_features:
            features = features + str(f) + " "
        print("if ", features)
    else:

        while user_name == "" or user_name in names:
            if user_name in names:
                user_name = str(input("Name already in use. Please enter another one: "))
            else:
                user_name = str(input("Please enter a name: "))

        print("\nEnter password and press TAB afterwards.")
        user_input = kb.read_input(1)
        password = user_input[1][0]

        if len(password) == 0:
            print("\nNo password entered.")
            return

        features = user_input[0]
    print("feat",features)

    print("\nPassword entered: " + str(password))
    print("\nFeatures measured:\n" + str(features))

    try:
        os.makedirs("users/" + user_name)
    except IOError:
        everything_fine = False

    """ Number of feature values (len(pwd) * 2 - 1) -> each character and delays between them """
    m = len(password) * 2 - 1
    print("\nNumber of coefficients: " + str(m))

    """ Create random r and q and save them to the file system """
    r = misc.generate_r(user_name)
    q = misc.generate_q(user_name)

    if r is False or q is False:
        everything_fine = False

    """ Create a random polynomial """
    polynomial = misc.generate_polynomial(q, m)
    print("\nThe hardened password is: " + str(polynomial[0]))

    """ Create the initial instruction table """
    inttable.init_instruction_table(user_name, polynomial, m, password, r, q)

    """ Try to encrypt the new history file with the new hpwd and save it """
    key = crypto.get_aes_key(polynomial[0]).digest()

    if demo: # there is a bug with feature handling somewhere...
        if not file_ops.write("users/" + user_name + "/history",
                              crypto.aes_encrypt(history.pad_history(features[:-1]), key), "wb"):
            everything_fine = False
    else:
        if not file_ops.write("users/" + user_name + "/history", crypto.aes_encrypt(history.pad_history(features), key), "wb"):
            everything_fine = False

    if not everything_fine:
        print(parameters.error_msg)
        try:
            os.remove("users/" + user_name)
        except IOError:
            return

        print("\nRemoved all newly created files.")
