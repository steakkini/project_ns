import parameters as parameters


def parse_features_from_history(history):
    """
    :param history: the history string including control strings (e.g. ---- BEGIN HISTORY ----)
    :return: a list of feature measurements
    parses the history text into a list containing lists of feature measurements
    """

    history = history.decode()
    features = history[0:history.find("\n#")]
    result = []

    for line in features.splitlines():
        line = line[:-1]
        print(line)
        print(type(line))
        result.append([int(i) for i in line.split(" ")])

    return result


def update_history(current_history, feature_vector):
    """
	:param current_history: current, plain text history
	:param feature_vector: features of the current logon attempt
	:return: the updated, plain text history

	updates the history file accordingly upon a successful login. the number of logins kept in the history file
	depends on the value assigned to parameters.h in the parameters list.
	"""

    new_login = []
    for i in feature_vector:
        new_login.append(int(i))

    current_history = parse_features_from_history(current_history)

    while len(current_history) >= parameters.h:
        current_history.pop(0)

    current_history.append(new_login)

    return current_history


def assemble_history(history):
    """
	:param history: list of feature measurements
	:return: the history string including pre/appended control strings and padding

	takes the nested list containing the feature measurement, converts everything into a string,
	pre/appends the control string and finally pads the history with 0s.
	"""

    history_string = ""
    for i in history:
        for j in i:
            history_string += str(j) + " "
        history_string += "\n"

    return pad_history(history_string[:-1])


def pad_history(to_be_padded):
    """
	:param to_be_padded: string which should be padded
	:return: string including appended padding

	appends a padding to a given input to a fixed output size using zeros;
	in this case to guarantee the fixed file size of the history file
	"""

    padding = len(to_be_padded) % 16

    if padding != 0:
        to_be_padded = to_be_padded + "\n" + ((16 - padding) * '#')

    return to_be_padded + ((parameters.history_size - len(to_be_padded)) * '#')
