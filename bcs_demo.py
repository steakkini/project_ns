import bcs_login as login
import bcs_register as register


def run_demo():
    register.register_new_user(demo=True)

    login.login_as_user(demo=True)

