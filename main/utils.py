import hashlib


def get_hash(file):
    res = hashlib.md5()
    while True:
        data = file.stream.read(128)
        res.update(data)
        if not data:
            break
        print(res)
    return res.hexdigest()
