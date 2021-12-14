from flask import request
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import exc
from sqlalchemy.orm import mapper

from Database.databaseAlchemy import db_session, metadata


# Classe Utente
class Utente(object):
    query = db_session.query_property()
    __tablename__ = 'Utente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(40), nullable=False)
    Cognome = Column(String(40), nullable=False)
    Username = Column(String(40), nullable=False, unique=True)
    Password = Column(String(30), nullable=False)
    Email = Column(String(120), nullable=False)
    Nazione = Column(String(30), nullable=False)
    Citta = Column(String(30), nullable=False)
    Provincia = Column(String(30), nullable=False)
    Via = Column(String(120), nullable=False)

    def __init__(self, nome, cognome, username, password, email, nazione, citta, provincia, via):
        self.Nome = nome
        self.Cognome = cognome
        self.Username = username
        self.Password = password
        self.Email = email
        self.Nazione = nazione
        self.Citta = citta
        self.Provincia = provincia
        self.Via = via

    def __repr__(self):
        return f'<User {self.Nome + self.Cognome + self.Username + self.Password + self.Email + self.Nazione + self.Citta + self.Provincia + self.Via!r}>'


# Mappatura della classe utente per inserimento nel database
utenti = Table('utenti', metadata,
               Column('id', Integer, primary_key=True, autoincrement=True),
               Column('Nome', String(40), nullable=False),
               Column('Cognome', String(40), nullable=False),
               Column('Username', String(40), nullable=False, unique=True),
               Column('Password', String(30), nullable=False),
               Column('Email', String(120), nullable=False),
               Column('Nazione', String(30), nullable=False),
               Column('Citta', String(30), nullable=False),
               Column('Provincia', String(30), nullable=False),
               Column('Via', String(120), nullable=False)
               )
mapper(Utente, utenti)


# Classe per la gestione delle eccezioni degli utente
class UserException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


# Metodo per leggere i campi dai vari form di registrazione per creare un nuovo utente
def form_user(db):
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        nazione = request.form['nazione']
        citta = request.form['citta']
        provincia = request.form['provincia']
        via = request.form['via']
        nuovo_utente = Utente(nome, cognome, username, password, email, nazione, citta, provincia, via)
        log_err = add_user(db, nuovo_utente)

        return log_err


# Metodo per aggiungere un nuovo utente al database
def add_user(db, utente_inserito):
    try:
        db.connect()
        nuovo_utente = utente_inserito
        if nuovo_utente is None:
            raise UserException("Utente non valido\n")
        else:
            db_session.add(nuovo_utente)
            db_session.commit()
    except exc.SQLAlchemyError as ex:
        print(ex.__doc__)
        return ex

    return None


# Metodo per leggere i campi dai vari form di login per effettuare la query di controllo
def form_login(db):
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']

        query_login = "SELECT * FROM utenti WHERE Username = %s AND Password = %s"
        valori_query = (username_form, password_form)
        utente = control_user(db, query_login, valori_query)
        if utente is None:
            return None
        return utente


# Metodo per effettuare una query di controllo sugli Username e password inseriti per accedere all'account
def control_user(db, query_login, valori_query):
    try:
        cursor = db.connect()
        result = cursor.execute(query_login, valori_query)
        utente = result.fetchone()
        db_session.commit()
    except exc.SQLAlchemyError as ex:
        print(ex.__doc__)
        return ex

    return utente
