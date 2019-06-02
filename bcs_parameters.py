"""
these parameters used to tweak the application and its behaviour
(e.g. number of h successful logins, thresholds, etc...)
"""

""" number of name-entering repetitions during registration """
rounds = 3

""" last h successful logins to the account (see section 3.1) """
h = 8

""" where k E R^+ is a parameter of the system (see section 3.1.) """
k = 10

""" size of q """
q_size = 160

""" size of r """
r_size = 160

""" 
file size in bytes of the history file 
resulting history file size = 16 (IV) + 1584 (history and padding) bytes
"""
history_size = 1584

""" binary writing mode """
bin_write = "wb"

""" text writing mode """
text_write = "w"

""" binary reading mode """
bin_read = "rb"

""" text reading mode """
text_read = "r"

""" generic error message """
error_msg = "Sorry some 1337 Error occurred!"

""" position of first feature measurement in history file """
pos = 24

""" size of AES IV"""
iv_size = 16