"""
    Gestion des requêtes de la table User
"""
from supabase import Client
import datetime

# Table utilisée pour les requêtes
from Database.Token import TokenTable

# Table utilisée pour le typage
from Database.Tables import User, SearchSettingsUser, UserType


class UserTable:
    db: Client
    tokenTable: TokenTable


    def __init__(self, db: Client, tokenTable: TokenTable):
        self.db = db
        self.tokenTable = tokenTable
        return

    def GetByPseudo(self, pseudo: str) -> User:
        """
            Récupère un utilisateur par son pseudo
            :param pseudo: Pseudo de l'utilisateur
            :return: Utilisateur
            :return: None si non trouvé
        """
        user = self.db.table('user').select("*").eq('pseudo', pseudo).execute().data
        if len(user) == 0:
            return None
        user = user[0]
        lastConnection: datetime.datetime = datetime.datetime.strptime(user["lastConnection"], "%Y-%m-%dT%H:%M:%S.%f")
        return User(user["id"], user["userTypeID"], user["pseudo"], user["password"], lastConnection, self.tokenTable.GetByUserID(user["id"]), user["picture"])

    def GetByID(self, id: int) -> User:
        """
            Récupère un utilisateur par son ID
            :param id: ID de l'utilisateur
            :return: Utilisateur
            :return: None si non trouvé
        """
        user = self.db.table('user').select("*").eq('id', id).execute().data
        if len(user) == 0:
            return None
        user = user[0]
        lastConnection: datetime.datetime = datetime.datetime.strptime(user["lastConnection"], "%Y-%m-%dT%H:%M:%S.%f")
        return User(user["id"], user["userTypeID"], user["pseudo"], user["password"], lastConnection, self.tokenTable.GetByUserID(user["id"]), user["picture"])

    def Search(self, searchSettings: SearchSettingsUser) -> list[User]:
        """
            Recherche des utilisateurs
            :param searchSettings: Paramètres de recherche
            :return: Liste d'utilisateurs
        """
        returnUsers: list[User] = []
        if searchSettings.isAdministrator:
            usersIDs: list = self.db.table('user').select("id").eq('userTypeID', searchSettings.isAdministrator).execute().data
            for userID in usersIDs:
                returnUsers.append(self.GetByID(userID[0]))
        if searchSettings.isBotaniste:
            usersIDs: list = self.db.table('user').select("id").eq('userTypeID', searchSettings.isBotaniste).execute().data
            for userID in usersIDs:
                returnUsers.append(self.GetByID(userID[0]))
        if searchSettings.isGardien:
            usersIDs: list = self.db.table('user').select("id").eq('userTypeID', searchSettings.isGardien).execute().data
            for userID in usersIDs:
                returnUsers.append(self.GetByID(userID[0]))
        return returnUsers



    def Add(self, user: User) -> User:
        """
            Ajoute un utilisateur
            :param user: Utilisateur à ajouter
            :return: Utilisateur ajouté
        """
        user.id = self.db.table('user').insert({"userTypeID": user.userTypeID, "pseudo": user.pseudo, "password": user.password, "lastConnection": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"), "picture": user.picture}).execute().data[0]["id"]
        return user

    def Delete(self, user: User) -> None:
        """
            Supprime un utilisateur
            :param user: Utilisateur à supprimer
        """
        self.db.table('user').delete().eq('id', user.id).execute()
        return
        