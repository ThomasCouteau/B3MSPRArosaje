import sqlite3worker
import datetime
from dataclasses import dataclass



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
    id: int
    userID: int
    accessToken: str
    refreshToken: str
    expire: datetime.datetime

@dataclass
class User:
    id: int
    userTypeID: UserType
    pseudo: str
    password: str
    lastConnection: datetime.datetime
    token: Token
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
        return User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], self.TokenGetByUserID(user[0][0]))
    def UserAdd(self, newUser: User) -> None:
        """
        Ajoute un utilisateur à la base de données
        :param newUser: Utilisateur à ajouter
        :return: None
        """
        self.db.execute("INSERT INTO User (userTypeID, pseudo, password, lastConnection) VALUES (?, ?, ?, ?)", [newUser.userTypeID, newUser.pseudo, newUser.password, datetime.datetime.now()])
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
        return Token(token[0][0], token[0][1], token[0][2], token[0][3], token[0][4])
    #########