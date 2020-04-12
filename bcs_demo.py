import bcs_login as login
import bcs_register as register
import csv
import os


def run_demo():

    with open('demo.csv', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)[1:]

    d_uname = data[0][1]
    d_password = data[0][2]
    d_features = [int(i) for i in data[0][3:]]

    try:
        os.remove("users/" + str(d_uname))
    except:
        IOError

    register.register_new_user(demo=True, d_uname=d_uname, d_password=d_password, d_features=d_features)

    success = []
    expected = []
    for attempt in data[1:]:
        if str(attempt[0]) == 'true':
            expected.append(True)
        else:
            expected.append(False)
        d_uname = attempt[1]
        d_password = attempt[2]
        d_features = [int(i) for i in attempt[3:]]

        success.append(login.login_as_user(demo=True, d_uname=d_uname, d_password=d_password, d_features=d_features))
    print("Expected: ", expected)
    print("Actual:   ", success)


