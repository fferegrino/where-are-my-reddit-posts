def read_keys(file):
    keys = {}
    with open(file, "r") as f:
        for l in f:
            etry = l.rstrip('\n').split(":")
            keys[etry[0]] = etry[1]
    return keys