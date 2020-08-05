import hashlib


def encrypt_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()


def calculate_md5(inp):
    return str(hashlib.md5(str(inp).encode()).hexdigest())
