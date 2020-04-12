from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Hash import SHA1, HMAC


def aes_encrypt(plain_text, key):
	"""
	:param plain_text: the text we want to encrypt
	:param key: the key derived from the password
	:return: the cipher text

	"""
	print("history ", plain_text)
	cipher = AES.new(key, AES.MODE_EAX)
	cipher_text, tag = cipher.encrypt_and_digest(plain_text.encode())
	return cipher.nonce, tag, cipher_text


def aes_decrypt(cipher_text, nonce, tag, key):
	"""
	:param cipher_text: the IV concatenated with the cipher text
	:param key: the key derived from the password
	:return: the plain text

	a simple AES decryption function which also retrieves the IV prepended to the cipher text
	"""

	try:
		cipher = AES.new(key, AES.MODE_EAX, nonce)
		return cipher.decrypt_and_verify(cipher_text, tag)
	except ValueError:
		print("Decryption Error :(")
		return None


def derive_key(password):
	"""
	:param password:
	:return: the SHA256 hash of the password (not the best practice, but tis just a PoC)

	"""

	return SHA256.new(data=str(password).encode())


def get_prf(password, r, i):
	"""
	:param password:
	:param r:
	:param i: for alpha -> 2 * i; for beta -> 2 * i + 1
	:return: HMAC

	"""

	return int(HMAC.new(password.encode(), r.encode(), SHA1).hexdigest(), 16) * i
