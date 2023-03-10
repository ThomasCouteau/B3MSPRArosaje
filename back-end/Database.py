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

@dataclass
class SearchSettingsUser:
    isBotaniste: bool
    isGardien: bool
    isAdministrator: bool
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
    creationDate: Union[datetime.datetime, None] = None
    picture: Union[str , None] = None
    comments: Union[list['Comment'], None] = None
###################


##### MESSAGERIE #####
@dataclass
class Conversation:
    id: Union[int, None] = None
    owner: Union[User, None] = None
    guardian: Union[User, None] = None

@dataclass
class PrivateMessage:
    id: Union[int, None] = None
    conversation: Union[Conversation, None] = None
    sender: Union[User, None]  = None
    message: Union[str, None] = None
    picture: Union[str, None] = None
    date: Union[datetime.datetime, None]  = None
######################


##### FORUM #####
@dataclass
class Comment:
    id: Union[int, None] = None
    planteID: Union[int, None] = None
    author: Union[User, None] = None
    message: Union[str, None] = None
    date: Union[datetime.datetime, None] = None
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
    def UserSearch(self, searchSettings: SearchSettingsUser) -> list[User]:
        """
        Recherche un utilisateur
        :param searchSettings: Paramètres de recherche
        :return: Liste d'utilisateur
        """
        request: str = "SELECT id FROM user WHERE "
        requestData: list = []
        if searchSettings.isBotaniste:
            request += "userTypeID = ?"
            requestData.append(UserType.BOTANISTE)
        if searchSettings.isGardien:
            if len(requestData) > 0:
                request += " OR "
                request += "userTypeID = ?"
            else:
                request += "userTypeID = ?"
            requestData.append(UserType.GARDIEN)
        if searchSettings.isAdministrator:
            if len(requestData) > 0:
                request += " OR "
                request += "userTypeID = ?"
            else:
                request += "userTypeID = ?"
            requestData.append(UserType.ADMIN)
        if searchSettings.isAdministrator:
            if len(requestData) > 0:
                request += " OR "
                request += "userTypeID = ?"
            else:
                request += "userTypeID = ?"
            requestData.append(UserType.ADMIN)

        usersIDs = self.db.execute(request, requestData)
        returnUsers: list[User] = []
        for userID in usersIDs:
            returnUsers.append(self.UserGetByID(userID[0]))
        return returnUsers


    def UserAdd(self, newUser: User) -> None:
        """
        Ajoute un utilisateur à la base de données
        :param newUser: Utilisateur à ajouter
        :return: None
        """
        self.db.execute("INSERT INTO User (userTypeID, pseudo, password, picture, lastConnection) VALUES (?, ?, ?, ?)", [newUser.userTypeID, newUser.pseudo, newUser.password,newUser.picture, datetime.datetime.now()])
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
        if returnPlantes.guardian != None:
            returnPlantes.guardian.password = None
            returnPlantes.guardian.token = None
        # Get all comments
        returnPlantes.comments = self.CommentGetByPlanteID(returnPlantes.id)
        return returnPlantes
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
            request += "ownerID = ?"
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

    def PlanteAdd(self, newPlante: Plante) -> int:
        """
        Ajoute une plante à la base de données
        :param newPlante: Plante à ajouter
        :return: planteID
        """
        self.db.execute("INSERT INTO plante (ownerID, name, statusID, latitude, longitude, picture) VALUES (?, ?, ?, ?, ?, ?)", [newPlante.owner.id, newPlante.name, PlanteStatus.DISPONIBLE, newPlante.latitude, newPlante.longitude, newPlante.picture])
        return self.db.execute("SELECT last_insert_rowid()")[0][0]
    def PlanteDelete(self, plante: Plante) -> None:
        """
        Supprime une plante
        :param plante: Plante à supprimer
        :return: None
        """
        self.db.execute("DELETE FROM plante WHERE id = ?", [plante.id])
        return
    def PlanteUpdate(self, plante: Plante) -> None:
        """
        Met à jour la plante
        :param plante: Plante
        :return: None
        """
        self.db.execute("UPDATE plante SET ownerID = ?, guardianID = ?, name = ?, statusID = ?, latitude = ?, longitude = ?, picture = ? WHERE id = ?", [plante.owner.id if plante.owner != None else None, plante.guardian.id if plante.guardian != None else None, plante.name, plante.status, plante.latitude, plante.longitude, plante.picture, plante.id])
        return
    ##########

    # CONVERSATION #
    def ConversationGetByUserID(self, userID: int) -> list[Conversation]:
        """
        Récupère toutes les conversations d'un utilisateur
        :param userID: ID de l'utilisateur
        :return: Liste de conversations
        """
        conversationsIDs = self.db.execute("SELECT id FROM conversation WHERE ownerID = ? OR guardianID = ?", [userID, userID])
        if len(conversationsIDs) == 0:
            return []
        returnConversations: list[Conversation] = []
        for conversationID in conversationsIDs:
            returnConversations.append(self.ConversationGetByID(conversationID[0]))
        return returnConversations
    def ConversationGetByID(self, conversationID: int) -> Conversation:
        """
        Récupère une conversation par son ID
        :param conversationID: ID de la conversation
        :return: Conversation
        """
        conversation = self.db.execute("SELECT id, ownerID, guardianID FROM conversation WHERE id = ?", [conversationID])
        if len(conversation) == 0:
            return []
        conversation = conversation[0]
        returnConversation: Conversation = Conversation(conversation[0], self.UserGetByID(conversation[1]) if conversation[1] != None else None, self.UserGetByID(conversation[2]) if conversation[2] != None else None)
        if returnConversation.owner != None:
            returnConversation.owner.password = None
            returnConversation.owner.token = None
        if returnConversation.guardian != None:
            returnConversation.guardian.password = None
            returnConversation.guardian.token = None
        return returnConversation
    def ConversationGetByUsersID(self, ownerID: int, guardianID: int) -> Conversation:
        """
        Récupère une conversation par les ID des utilisateurs
        :param ownerID: ID du propriétaire
        :param guardianID: ID du gardien
        :return: Conversation ou None
        """
        conversation = self.db.execute("SELECT id, ownerID, guardianID FROM conversation WHERE ownerID = ? AND guardianID = ?", [ownerID, guardianID])
        if len(conversation) == 0:
            return None
        conversation = conversation[0]
        returnConversation: Conversation = Conversation(conversation[0], self.UserGetByID(conversation[1]) if conversation[1] != None else None, self.UserGetByID(conversation[2]) if conversation[2] != None else None)
        if returnConversation.owner != None:
            returnConversation.owner.password = None
            returnConversation.owner.token = None
        if returnConversation.guardian != None:
            returnConversation.guardian.password = None
            returnConversation.guardian.token = None
        return returnConversation
    def MessageIDsGetByConversationID(self, conversationID: int) -> list[int]:
        """
        Récupère tous les messages d'une conversation
        :param conversationID: ID de la conversation
        :return: Liste des IDs des messages
        """
        messages = self.db.execute("SELECT id FROM privateMessage WHERE conversationID = ? ORDER BY id DESC", [conversationID])
        if len(messages) == 0:
            return []
        returnMessagesID: list[int] = []
        for message in messages:
            returnMessagesID.append(message[0])
        return returnMessagesID
    def MessageGetByID(self, messageID: int) -> PrivateMessage:
        """
        Récupère un message par son ID
        :param messageID: ID du message
        :return: Message
        """
        message = self.db.execute("SELECT id, conversationID, senderID, message, picture, date FROM privateMessage WHERE id = ?", [messageID])
        if len(message) == 0:
            return None
        message = message[0]
        returnMessage: PrivateMessage = PrivateMessage(message[0], self.ConversationGetByID(message[1]), self.UserGetByID(message[2]), message[3], message[4])
        returnMessage.sender.password = None
        returnMessage.sender.token = None
        return returnMessage

    def ConversationAdd(self, newConversation: Conversation) -> int:
        """
        Ajoute une conversation à la base de données
        :param newConversation: Conversation à ajouter
        :return: conversationID
        """
        self.db.execute("INSERT INTO conversation (ownerID, guardianID) VALUES (?, ?)", [newConversation.owner.id, newConversation.guardian.id])
        return self.db.execute("SELECT last_insert_rowid()")[0][0]
    def MessageAdd(self, newMessage: PrivateMessage) -> int:
        """
        Ajoute un message à la base de données
        :param newMessage: Message à ajouter
        :return: messageID
        """
        self.db.execute("INSERT INTO privateMessage (conversationID, senderID, message, picture) VALUES (?, ?, ?, ?)", [newMessage.conversation.id, newMessage.sender.id, newMessage.message, newMessage.picture])
        return self.db.execute("SELECT last_insert_rowid()")[0][0]
    ################

    # COMMENTS #
    def CommentGetByPlanteID(self, plantID: int) -> list[Comment]:
        """
        Récupère tous les commentaires d'une plante
        :param plantID: ID de la plante
        :return: Liste de commentaires
        """
        comments = self.db.execute("SELECT id FROM comment WHERE planteID = ? ORDER BY id DESC", [plantID])
        if len(comments) == 0:
            return []
        returnComments: list[Comment] = []
        for comment in comments:
            returnComments.append(self.CommentGetByID(comment[0]))
        return returnComments
    def CommentGetByID(self, commentID: int) -> Comment:
        """
        Récupère un commentaire par son ID
        :param commentID: ID du commentaire
        :return: Commentaire
        """
        comment = self.db.execute("SELECT id, planteID, authorID, message, date FROM comment WHERE id = ?", [commentID])
        if len(comment) == 0:
            return None
        comment = comment[0]
        returnComment: Comment = Comment(comment[0], comment[1], self.UserGetByID(comment[2]), comment[3], comment[4])
        returnComment.author.password = None
        returnComment.author.token = None
        return returnComment

    def CommentAdd(self, newComment: Comment) -> int:
        """
        Ajoute un commentaire à la base de données
        :param newComment: Commentaire à ajouter
        :return: commentID
        """
        self.db.execute("INSERT INTO comment (planteID, authorID, message) VALUES (?, ?, ?)", [newComment.plante.id, newComment.author.id, newComment.message])
        return self.db.execute("SELECT last_insert_rowid()")[0][0]
    def CommentDelete(self, commentID: int):
        """
        Supprime un commentaire de la base de données
        :param commentID: ID du commentaire à supprimer
        """
        self.db.execute("DELETE FROM comment WHERE id = ?", [commentID])
    ############