import hashlib


def encrypt_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()
