def read_keys(file: str) -> dict:
    """
    Read a file containing the reddit credentials with the format:
        client_id:YOUR REDDIT'S CLIENT ID
        client_secret:YOUR REDDIT'S CLIENT SECRET
        password:YOUR REDDIT'S ACCOUNT PASSSWORD
        username:YOUR REDDIT'S USERNAME
    :param file: the path to the file
    :return: a dictionary containing four entries:
        client_id, client_secret, password, username
    """
    keys = {}
    with open(file, "r") as f:
        for l in f:
            etry = l.rstrip('\n').split(":")
            keys[etry[0]] = etry[1]
    return keys
