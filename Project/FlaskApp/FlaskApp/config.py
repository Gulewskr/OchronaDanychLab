class Config(object):
    #klucz do szyfrowania sesji użytkownika
    SECRET_KEY = 'secret-key-goes-here'
    #adress do bazy danych
    SQLALCHEMY_DATABASE_URL = 'sqlite:///db.sqlite'
    #pieprz do haseł
    PEPPER = b'p23k23o3'
    #key do szyfrowania notatek
    NOTEKEY = 'klucz'