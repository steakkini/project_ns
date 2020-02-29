from Crypto.Cipher import AES
import os
import bcrypt
import bcs_parameters as parameters
import hmac
import hashlib


def aes_encrypt(plain_text, key):
	"""
	:param plain_text: the text we want to encrypt
	:param key: the key derived from the password
	:return: the cipher text

	AES encryption function which also
	generates a suitable IV
	"""

	iv = os.urandom(parameters.iv_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return iv + cipher.encrypt(plain_text)


def aes_decrypt(cipher_text, key):
	"""
	:param cipher_text: the IV concatenated with the cipher text
	:param key: the key derived from the password
	:return: the plain text

	a simple AES decryption function which also retrieves the IV prepended to the cipher text
	"""

	iv = cipher_text[0:parameters.iv_size]
	cipher_text = cipher_text[parameters.iv_size:len(cipher_text)]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return cipher.decrypt(cipher_text)


def derive_key(password):
	"""
	:param password: the password we want to derive the key from
	:return: the derived key

	this is just wrapper function for bcrypt. the KDF function might be replaced in the future without any hassle :)
	"""

	key = bcrypt.kdf(
		password=password,
		salt="thisdoesnotreallymatterhere",  # not using random salts, because I am lazy and it does not really matter here
		desired_key_bytes=32,
		rounds=120)
	
	return key


def get_alpha_prf(pwd, r, i):
	return int(hmac.new(pwd, r, hashlib.sha1).hexdigest(), 16) * (2 * i)


def get_beta_prf(pwd, r, i):
	return int(hmac.new(pwd, r, hashlib.sha1).hexdigest(), 16) * (2 * i + 1)
