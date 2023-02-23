"""
    Gestion des requêtes de la table PrivateMessage
"""
from supabase import Client
import datetime

# Table utilisée pour les requêtes
from Database.User import UserTable
from Database.Comment import CommentTable

# Table utilisée pour le typage
from Database.Tables import PrivateMessage


class PrivateMessageTable:
    db: Client
    userTable: UserTable
    commentTable: CommentTable

    def __init__(self, db: Client, userTable: UserTable, commentTable: CommentTable):
        self.db = db
        self.userTable = userTable
        self.commentTable = commentTable
        return
        
    def MessageIDsGetByConversationID(self, conversationID: int) -> list[int]:
        """
            Récupère tous les messages d'une conversation
            :param conversationID: ID de la conversation
            :return: Liste des IDs des messages
        """
        messages = self.db.table('privateMessage').select("id").eq('conversationID', conversationID).order('id', ascending=False).execute().data
        if len(messages) == 0:
            return []
        returnMessagesID: list[int] = []
        for message in messages:
            returnMessagesID.append(message["id"])
        return returnMessagesID
    
    def GetByID(self, messageID: int) -> PrivateMessage:
        """
            Récupère un message par son ID
            :param messageID: ID du message
            :return: Message
        """
        message = self.db.table('privateMessage').select("*").eq('id', messageID).execute().data
        if len(message) == 0:
            return None
        message = message[0]
        returnMessage = PrivateMessage(
            message["id"],
            self.commentTable.GetByID(message["conversationID"]) if message["conversationID"] != None else None,
            self.userTable.GetByID(message["senderID"]) if message["senderID"] != None else None,
            message["message"],
            message["picture"]
        )
        returnMessage.sender.password = None
        returnMessage.sender.token = None
        return returnMessage

    def Add(self, newMessage: PrivateMessage) -> int:
        """
            Ajoute un message à la base de données
            :param newMessage: Message à ajouter
            :return: messageID
        """
        id = self.db.table('privateMessage').insert([
            {
                "conversationID": newMessage.conversation.id,
                "senderID": newMessage.sender.id,
                "message": newMessage.message,
                "picture": newMessage.picture
            }
        ]).execute().data
        return id[0]["id"]