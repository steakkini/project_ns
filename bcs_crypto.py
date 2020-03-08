from Crypto.Cipher import AES

import bcrypt
import hmac
import hashlib


def aes_encrypt(plain_text, key):
	"""
	:param plain_text: the text we want to encrypt
	:param key: the key derived from the password
	:return: the cipher text

	"""

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
	:param password: the password we want to derive the key from
	:return: the derived key

	this is just wrapper function for bcrypt. the KDF function might be replaced in the future without any hassle :)
	"""

	key = bcrypt.kdf(
		password=password.encode(),
		salt="thisdoesnotreallymatterhere".encode(),  # not using random salts, because I am lazy and it does not really matter here
		desired_key_bytes=32,
		rounds=120)
	
	return key


def get_alpha_prf(pwd, r, i):
	return int(hmac.new(pwd.encode(), r.encode(), hashlib.sha1).hexdigest(), 16) * (2 * i)


def get_beta_prf(pwd, r, i):
	return int(hmac.new(pwd.encode(), r.encode(), hashlib.sha1).hexdigest(), 16) * (2 * i + 1)
