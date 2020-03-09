"""
These parameters are used to tweak the application and its behaviour.
"""


""" last h successful logins to the account (see section 3.1) """
h = 10

""" where k E R^+ is a parameter of the system (see section 3.1.) """
""" assumed to be a feature threshold to filter out unrealistic deviations (e.g. a delay of 2 seconds) """
k = 2

""" threshold of the features """
threshold = 10

""" size of cryptographic primitives q, r, hashes """
crypto_size = 160

""" 
file size in bytes of the history file 
resulting history file size = 16 (IV) + 1584 (history and padding) bytes
"""
history_size = 1584

""" generic error message """
error_msg = "Sorry some 1337 Error occurred!"

""" position of first feature measurement in history file """
pos = 24

