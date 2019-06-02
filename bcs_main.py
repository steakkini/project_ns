"""
This is a prototype implementation for password hardening
which is based on the paper "Password hardening based on keystroke dynamics"
by Fabian Monrose, Michael K. Reiter and Susanne Wetzel (Springer-Verlag, 2001).
"""

import bcs_login as login
import bcs_register as register
import bcs_demo as demo

while True:
	option = ""
	
	print("\n[0] Login" + "\n[1] Register" + "\n[2] Exit" + "\n[3] Demo")

	while option not in ["0", "1", "2", "3"]:
		option = raw_input("Select an option: ")
	
	if option == "0":
		login.login_as_user()

	if option == "1":
		register.register_new_user()
	
	if option == "2":
		print("Good Bye!")
		exit()

	if option == "3":
		demo.run_demo()
