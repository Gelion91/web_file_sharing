import hashlib


def get_hash(file):
    res = hashlib.md5()
    res.update(file.read())
    return res.hexdigest()
