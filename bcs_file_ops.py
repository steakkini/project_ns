def write(path, content, mode):
	"""
	:param path: the relative path including the file name
	:param content: the content to be written to the file
	:param mode: text vs binary mode
	:return: True if successful, False otherwise
	"""

	try:
		with open(path, mode) as f:
			f.write(content)
			return True
	except IOError:
		return False


def read(path, mode):
	"""
	:param path: the relative path including the file name
	:param mode: text vs binary mode
	:return: the file's content if successful, False otherwise
	"""
	try:
		with open(path, mode) as f:
			return f.read()
	except IOError:
		return False
