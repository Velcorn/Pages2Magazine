from configparser import ConfigParser


def login_config(filename="login.ini", section="api"):
    parser = ConfigParser()
    parser.read(filename)
    login = {}
    params = parser.items(section)
    for param in params:
        login[param[0]] = param[1]
    return login
