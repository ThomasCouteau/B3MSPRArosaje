"""
    Gestion des requêtes de la table Conversation
"""
from supabase import Client
import datetime

# Table utilisée pour les requêtes
from Database.User import UserTable
from Database.Conversation import ConversationTable

# Table utilisée pour le typage
from Database.Tables import Conversation


class ConversationTable:
    db: Client
    userTable: UserTable
    conversationTable: ConversationTable

    def __init__(self, db: Client, userTable: UserTable, conversationTable: ConversationTable):
        self.db = db
        self.userTable = userTable
        self.conversationTable = conversationTable
        return

    def GetByUserID(self, userID: int) -> list[Conversation]:
        """
            Récupère toutes les conversations d'un utilisateur
            :param userID: ID de l'utilisateur
            :return: Liste de conversations
        """
        conversationsFromOwner: list = self.db.table('conversation').select("*").eq('ownerID', userID).execute().data
        conversationsFromGuardian: list = self.db.table('conversation').select("*").eq('guardianID', userID).execute().data
        conversations = conversationsFromOwner + conversationsFromGuardian
        if len(conversations) == 0:
            return []
        returnConversations: list[Conversation] = []
        for conversation in conversations:
            returnConversations.append(
                Conversation(
                    conversation["id"],
                    self.userTable.GetByID(conversation["ownerID"]) if conversation["ownerID"] != None else None,
                    self.userTable.GetByID(conversation["guardianID"]) if conversation["guardianID"] != None else None
                )
            )
        return returnConversations

    def GetByID(self, conversationID: int) -> Conversation:
        """
            Récupère une conversation par son ID
            :param conversationID: ID de la conversation
            :return: Conversation
        """
        conversation = self.db.table('conversation').select("*").eq('id', conversationID).execute().data
        if len(conversation) == 0:
            return []
        conversation = conversation[0]
        returnConversation = Conversation(
            conversation["id"],
            self.userTable.GetByID(conversation["ownerID"]) if conversation["ownerID"] != None else None,
            self.userTable.GetByID(conversation["guardianID"]) if conversation["guardianID"] != None else None
        )
        if returnConversation.owner != None:
            returnConversation.owner.password = None
            returnConversation.owner.token = None
        if returnConversation.guardian != None:
            returnConversation.guardian.password = None
            returnConversation.guardian.token = None
        return returnConversation

    def GetByUsersID(self, ownerID: int, guardianID: int) -> Conversation:
        """
            Récupère une conversation par les ID des utilisateurs
            :param ownerID: ID du propriétaire
            :param guardianID: ID du gardien
            :return: Conversation ou None
        """
        conversation = self.db.table('conversation').select("*").eq('ownerID', ownerID).eq('guardianID', guardianID).execute().data
        if len(conversation) == 0:
            return None
        conversation = conversation[0]
        returnConversation = Conversation(
            conversation["id"],
            self.userTable.GetByID(conversation["ownerID"]) if conversation["ownerID"] != None else None,
            self.userTable.GetByID(conversation["guardianID"]) if conversation["guardianID"] != None else None
        )
        if returnConversation.owner != None:
            returnConversation.owner.password = None
            returnConversation.owner.token = None
        if returnConversation.guardian != None:
            returnConversation.guardian.password = None
            returnConversation.guardian.token = None
        return returnConversation

    def Add(self, newConversation: Conversation) -> int:
        """
            Ajoute une conversation à la base de données
            :param newConversation: Conversation à ajouter
            :return: conversationID
        """
        id = self.db.table('conversation').insert([
            {
                "ownerID": newConversation.owner.id,
                "guardianID": newConversation.guardian.id
            }
        ]).execute().data
        return id[0]["id"]