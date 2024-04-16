class User:
    def __init__(self, username, password, privateKey, publicKey):
        self._username = username
        self._password = password
        self._privateKey = privateKey
        self._publicKey = publicKey

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def privateKey(self):
        return self._privateKey

    @property
    def publicKey(self):
        return self._publicKey
