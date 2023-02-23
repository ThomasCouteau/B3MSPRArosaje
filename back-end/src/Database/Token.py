"""
    Gestion des requêtes de la table Token
"""
from supabase import Client
import datetime
import random

# Table utilisée pour le typage
from Database.Tables import Token, User



class TokenTable:
    db: Client
    

    def __init__(self, db: Client):
        self.db = db
        return

    def GetByUserID(self, userID: int) -> Token:
        """
            Récupère un token par son ID
            :param userID: ID de l'utilisateur
            :return: Token
        """
        token = self.db.table('token').select("*").eq('userID', userID).execute().data
        if len(token) == 0:
            return None
        token = token[0]
        expire: datetime.datetime = datetime.datetime.strptime(token["expire"], "%Y-%m-%dT%H:%M:%S.%f")
        return Token(token["id"], token["userID"], token["accessToken"], token["refreshToken"], expire)

    def GetByAccessToken(self, accessToken: str) -> Token:
        """
            Récupère un token par son token d'accès
            :param accessToken: Token d'accès
            :return: Token
        """
        token = self.db.table('token').select("*").eq('accessToken', accessToken).execute().data
        if len(token) == 0:
            return None
        token = token[0]
        expire: datetime.datetime = datetime.datetime.strptime(token["expire"], "%Y-%m-%dT%H:%M:%S.%f")
        return Token(token["id"], token["userID"], token["accessToken"], token["refreshToken"], expire)

    def GetByRefreshToken(self, refreshToken: str) -> Token:
        """
            Récupère un token par son token de rafraichissement
            :param refreshToken: Token de rafraichissement
            :return: Token
        """
        token = self.db.table('token').select("*").eq('refreshToken', refreshToken).execute().data
        if len(token) == 0:
            return None
        token = token[0]
        expire: datetime.datetime = datetime.datetime.strptime(token["expire"], "%Y-%m-%dT%H:%M:%S.%f")
        return Token(token["id"], token["userID"], token["accessToken"], token["refreshToken"], expire)



    def Generate(self, user: User) -> Token:
        """
            Génère un token pour un utilisateur
            :param user: Utilisateur
            :return: None
        """
        accessToken = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=64))
        refreshToken = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=64))
        if user.token is not None:                                                                                      # Si l'utilisateur a déjà un token
            self.db.table('token').update({"accessToken": accessToken, "refreshToken": refreshToken, "expire": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S.%f")}).eq('userID', user.id).execute()
        else:                                                                                                           # Si l'utilisateur n'a pas de token
            self.db.table('token').insert({"userID": user.id, "accessToken": accessToken, "refreshToken": refreshToken, "expire": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S.%f")}).execute()
        return self.GetByRefreshToken(refreshToken)

    def Refresh(self, token: Token) -> Token:
        """
            Rafraichit un token d'accès par son token de rafraichissement
            :param token: Token
            :return: None
        """
        accessToken = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=64))
        refreshToken = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=64))
        self.db.table('token').update({"accessToken": accessToken, "refreshToken": refreshToken, "expire": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S.%f")}).eq('refreshToken', token.refreshToken).execute()
        return self.GetByRefreshToken(refreshToken)

    def Delete(self, user: User) -> None:
        """
            Supprime un token
            :param user: Utilisateur
            :return: None
        """
        self.db.table('token').delete().eq('userID', user.id).execute()
        return