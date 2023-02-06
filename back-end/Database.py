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


##### SEARCH SETTINGS #####
@dataclass
class SearchSettings:
    availablePlante: bool
    keptPlante: bool
    donePlante: bool
    ownerID: int
    guardianID: int
    latitude: float
    longitude: float
    radius: int
###########################


##### PLANTES #####
@dataclass
class PlanteStatus:
    DISPONIBLE: int = 1
    GARDE: int = 2
    FINI: int = 3

    def __to_string__(self, id: int) -> str:
        if id == 1:
            return "Disponible"
        elif id == 2:
            return "Gardé"
        elif id == 3:
            return "Fini"
        else:
            return "Inconnu"

@dataclass
class Plante:
    id: Union[int, None] = None
    owner: Union[User, None] = None
    guardian: Union[User, None] = None
    name: Union[str, None] = None
    status: Union[PlanteStatus, int, None] = None
    latitude: Union[float, None] = None
    longitude: Union[float, None] = None
    creationDate: Union[datetime.datetime , None] = None
    picture: Union[bytes , None] = None
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

    # PLANTE #
    def PlanteGetByID(self, planteID: int) -> Plante:
        """
        Récupère une plante par son ID
        :param planteID: ID de la plante
        :return: Plante
        """
        plante = self.db.execute("SELECT id, ownerID, guardianID, name, statusID, latitude, longitude, creationDate, picture FROM plante WHERE id = ?", [planteID])
        if len(plante) == 0:
            return None
        plante = plante[0]
        returnPlantes: Plante = Plante(plante[0], self.UserGetByID(plante[1]) if plante[1] != None else None, self.UserGetByID(plante[2]) if plante[2] != None else None, plante[3], plante[4], plante[5], plante[6], datetime.datetime.strptime(plante[7], "%Y-%m-%d %H:%M:%S"), plante[8])
        if returnPlantes.owner != None:
            returnPlantes.owner.password = None
            returnPlantes.owner.token = None
            returnPlantes.owner.picture = None
            returnPlantes.owner.lastConnection = None
        if returnPlantes.guardian != None:
            returnPlantes.guardian.password = None
            returnPlantes.guardian.token = None
            returnPlantes.guardian.picture = None
            returnPlantes.guardian.lastConnection = None
        return returnPlantes

    def PlanteAdd(self, newPlante: Plante) -> int:
        """
        Ajoute une plante à la base de données
        :param newPlante: Plante à ajouter
        :return: planteID
        """
        self.db.execute("INSERT INTO plante (ownerID, name, statusID, latitude, longitude, picture) VALUES (?, ?, ?, ?, ?, ?)", [newPlante.owner.id, newPlante.name, PlanteStatus.DISPONIBLE, newPlante.latitude, newPlante.longitude, newPlante.picture])
        return self.db.execute("SELECT last_insert_rowid()")[0][0]
    def PlanteSearchAll(self, searchSettings: SearchSettings) -> list[Plante]:
        """
        Récupère toutes les plantes de la base de données
        :param searchSettings: Paramètres de recherche
        :return: Liste de plantes
        """
        request: str = "SELECT id FROM plante WHERE "
        requestData: list = []
        if searchSettings.availablePlante:
            request += "(statusID = ?"
            requestData.append(PlanteStatus.DISPONIBLE)
        if searchSettings.keptPlante:
            if len(requestData) > 0:
                request += " OR "
                request += "statusID = ?"
            else:
                request += "(statusID = ?"
            requestData.append(PlanteStatus.GARDE)
        if searchSettings.donePlante:
            if len(requestData) > 0:
                request += " OR "
                request += "statusID = ?"
            else:
                request += "(statusID = ?"
            requestData.append(PlanteStatus.FINI)
        if searchSettings.availablePlante or searchSettings.keptPlante or searchSettings.donePlante:
            request += ")"

        if searchSettings.ownerID != -1:
            if len(requestData) > 0:
                request += " AND "
            request += "ownerID = ?"é
            requestData.append(searchSettings.ownerID)
        if searchSettings.guardianID != -1:
            if len(requestData) > 0:
                request += " AND "
            request += "guardianID = ?"
            requestData.append(searchSettings.guardianID)
        if searchSettings.latitude != -1 and searchSettings.longitude != -1 and searchSettings.radius != -1:
            if len(requestData) > 0:
                request += " AND "
            request += "latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?"
            requestData.append(searchSettings.latitude - searchSettings.radius)
            requestData.append(searchSettings.latitude + searchSettings.radius)
            requestData.append(searchSettings.longitude - searchSettings.radius)
            requestData.append(searchSettings.longitude + searchSettings.radius)
        request += " ORDER BY id DESC"

        plantesIDs = self.db.execute(request, requestData)
        returnPlantes: list[Plante] = []
        for planteID in plantesIDs:
            returnPlantes.append(self.PlanteGetByID(planteID[0]))
        return returnPlantes
    def PlanteDelete(self, plante: Plante) -> None:
        """
        Supprime une plante
        :param plante: Plante à supprimer
        :return: None
        """
        self.db.execute("DELETE FROM plante WHERE id = ?", [plante.id])
        return
    ##########

    