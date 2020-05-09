import hashlib


def encrypt_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()


def convert_and_compare_plain_passwords(old_password, new_password):
    pass1 = old_password
    pass2 = new_password
    pass
