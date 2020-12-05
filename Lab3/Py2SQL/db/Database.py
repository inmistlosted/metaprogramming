class Database(object):
    def __init__(self, host, port, name, username, password):
        self.__host = host
        self.__port = port
        self.__name = name
        self.__username = username
        self.__password = password

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def name(self):
        return self.__name

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password
