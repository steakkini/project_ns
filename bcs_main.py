"""
This is a prototype implementation for password hardening
which is based on the paper "Password hardening based on keystroke dynamics"
by Fabian Monrose, Michael K. Reiter and Susanne Wetzel (Springer-Verlag, 2001).
"""

import bcs_demo as demo
import bcs_login as login
import bcs_register as register


def main():
	while True:
		option = ""

		print("\n[0] Login" + "\n[1] Register" + "\n[2] Demo" + "\n[3] Exit")

		while option not in ["0", "1", "2", "3"]:
			option = input("\nSelect an option: ")

		if option == "0":
			login.login_as_user(demo=False, d_uname="", d_password="", d_features=[])

		if option == "1":
			register.register_new_user(demo=False, d_uname="", d_password="", d_features=[])

		if option == "2":
			demo.run_demo()

		if option == "3":
			print("Good Bye!")
			exit()


if __name__ == '__main__':
	main()
