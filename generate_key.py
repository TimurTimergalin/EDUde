import hashlib


def generate_key(user):  # Teacher или Student, не User
    return hashlib.md5(f'{user.surname}{user.name}{user.hashed_password}'.encode('utf-8')).hexdigest()
