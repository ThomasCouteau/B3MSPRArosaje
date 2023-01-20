import sqlite3worker
import datetime
from dataclasses import dataclass
from typing import Union
import random



##### AUTH #####
@dataclass
class UserType:
    BOTANISTE: int = 1
    ADMIN: int = 2
    GARDIEN: int = 3

    def __to_string__(self, id: int) -> str:
        if id == 1:
            return "Botaniste"
        elif id == 2:
            return "Admin"
        elif id == 3:
            return "Gardien"
        else:
            return "Inconnu"

@dataclass
class Token:
    id: Union[int, None] = None
    userID: Union[int, None] = None
    accessToken: Union[str, None] = None
    refreshToken: Union[str, None] = None
    expire: Union[datetime.datetime, None] = None

@dataclass
class User:
    id: Union[int, None] = None
    userTypeID: Union[UserType, int, None] = None
    pseudo: Union[str, None] = None
    password: Union[str, None] = None
    lastConnection: Union[datetime.datetime, None] = None
    token: Union[Token, None] = None
    picture: Union[str, None] = None
###############


##### PLANTES #####
@dataclass
class PlanteStatus:
    DEMANDE: int = 1
    GARDE: int = 2
    RECUPERE: int = 3

    def __to_string__(self, id: int) -> str:
        if id == 1:
            return "Demandé"
        elif id == 2:
            return "Gardé"
        elif id == 3:
            return "Recuperé"
        else:
            return "Inconnu"

@dataclass
class Plante:
    id: int
    owner: User
    guardian: User
    name: str
    status: PlanteStatus
    latitude: float
    longitude: float
    creationDate: datetime.datetime
###################


##### MESSAGERIE #####
@dataclass
class Conversation:
    id: int
    owner: User
    guardian: User

@dataclass
class PrivateMessage:
    id: int
    conversation: Conversation
    sender: User
    message: str
    image: str
    date: datetime.datetime
######################


##### FORUM #####
@dataclass
class Post:
    id: int
    author: User
    plante: Plante
    title: str
    picture: str
    date: datetime.datetime

@dataclass
class Comment:
    id: int
    post: Post
    author: User
    message: str
    date: datetime.datetime
#################



class Database:
    db: sqlite3worker.Sqlite3Worker

    def __init__(self, db_path: str) -> None:
        self.db = sqlite3worker.Sqlite3Worker(db_path)
        return

    # USER #
    def UserGetByPseudo(self, id: int) -> User:
        """
        Récupère un utilisateur par son pseudo
        :param pseudo: Pseudo de l'utilisateur
        :return: Utilisateur
        :return: None si non trouvé
        """
        user = self.db.execute("SELECT * FROM User WHERE pseudo = ?", [id])
        if len(user) == 0:
            return None
        date = datetime.datetime.strptime(user[0][4], "%Y-%m-%d %H:%M:%S.%f")
        return User(user[0][0], user[0][1], user[0][2], user[0][3], date, self.TokenGetByUserID(user[0][0]), user[0][5])
    def UserGetByID(self, id: int) -> User:
        """
        Récupère un utilisateur par son ID
        :param id: ID de l'utilisateur
        :return: Utilisateur
        :return: None si non trouvé
        """
        user = self.db.execute("SELECT * FROM User WHERE id = ?", [id])
        if len(user) == 0:
            return None
        date = datetime.datetime.strptime(user[0][4], "%Y-%m-%d %H:%M:%S.%f")
        return User(user[0][0], user[0][1], user[0][2], user[0][3], date, self.TokenGetByUserID(user[0][0]), user[0][5])

    def UserAdd(self, newUser: User) -> None:
        """
        Ajoute un utilisateur à la base de données
        :param newUser: Utilisateur à ajouter
        :return: None
        """
        self.db.execute("INSERT INTO User (userTypeID, pseudo, password, lastConnection) VALUES (?, ?, ?, ?)", [newUser.userTypeID, newUser.pseudo, newUser.password, datetime.datetime.now()])
        return
    def UserDelete(self, user: User) -> None:
        """
        Supprime un utilisateur de la base de données
        :param user: Utilisateur à supprimer
        :return: None
        """
        self.db.execute("DELETE FROM User WHERE id = ?", [user.id])
        return
    ########

    # TOKEN #
    def TokenGetByUserID(self, userID: int) -> Token:
        """
        Récupère un token par son ID
        :param userID: ID de l'utilisateur
        :return: Token
        """
        token = self.db.execute("SELECT * FROM Token WHERE userID = ?", [userID])
        if len(token) == 0:
            return None
        expire: datetime.datetime = datetime.datetime.strptime(token[0][4], "%Y-%m-%d %H:%M:%S.%f")
        return Token(token[0][0], token[0][1], token[0][2], token[0][3], expire)
    def TokenGetByAccessToken(self, accessToken: str) -> Token:
        """
        Récupère un token par son token d'accès
        :param accessToken: Token d'accès
        :return: Token
        """
        token = self.db.execute("SELECT * FROM Token WHERE accessToken = ?", [accessToken])
        if len(token) == 0:
            return None
        expire: datetime.datetime = datetime.datetime.strptime(token[0][4], "%Y-%m-%d %H:%M:%S.%f")
        return Token(token[0][0], token[0][1], token[0][2], token[0][3], expire)
    def TokenGetByRefreshToken(self, refreshToken: str) -> Token:
        """
        Récupère un token par son token de rafraichissement
        :param refreshToken: Token de rafraichissement
        :return: Token
        """
        token = self.db.execute("SELECT * FROM Token WHERE refreshToken = ?", [refreshToken])
        if len(token) == 0:
            return None
        expire: datetime.datetime = datetime.datetime.strptime(token[0][4], "%Y-%m-%d %H:%M:%S.%f")
        return Token(token[0][0], token[0][1], token[0][2], token[0][3], expire)

    def TokenGenerate(self, user: User) -> Token:
        """
        Génère un token pour un utilisateur
        :param user: Utilisateur
        :return: None
        """
        accessToken = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=64))
        refreshToken = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=64))
        if user.token is not None:                                                                                      # Si l'utilisateur a déjà un token
            self.db.execute("UPDATE Token SET accessToken = ?, refreshToken = ?, expire = ? WHERE userID = ?", [accessToken, refreshToken, datetime.datetime.now() + datetime.timedelta(days=1), user.id])
        else:                                                                                                           # Si l'utilisateur n'a pas de token
            self.db.execute("INSERT INTO Token (userID, accessToken, refreshToken, expire) VALUES (?, ?, ?, ?)", [user.id, accessToken, refreshToken, datetime.datetime.now() + datetime.timedelta(days=1)])
        return self.TokenGetByRefreshToken(refreshToken)
    def TokenRefresh(self, token: Token) -> Token:
        """
        Rafraichit un token d'accès par son token de rafraichissement
        :param token: Token
        :return: None
        """
        accessToken = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=64))
        refreshToken = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=64))
        self.db.execute("UPDATE token SET accessToken = ?, refreshToken = ?, expire = ? WHERE refreshToken = ?", [accessToken, refreshToken, datetime.datetime.now() + datetime.timedelta(days=1), token.refreshToken])
        return self.TokenGetByRefreshToken(refreshToken)
    def TokenDelete(self, user: User) -> None:
        """
        Supprime un token
        :param user: Utilisateur
        :return: None
        """
        self.db.execute("DELETE FROM Token WHERE userID = ?", [user.id])
        return
    #########