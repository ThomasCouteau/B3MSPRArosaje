"""
    Gestion des requêtes de la table Comment
"""
from supabase import Client
import datetime

# Table utilisée pour les requêtes
from Database.User import UserTable

# Table utilisée pour le typage
from Database.Tables import Comment


class CommentTable:
    db: Client
    userTable: UserTable


    def __init__(self, db: Client, userTable: UserTable):
        self.db = db
        self.userTable = userTable
        return

    def GetByPlanteID(self, plantID: int) -> list[Comment]:
        """
            Récupère tous les commentaires d'une plante
            :param plantID: ID de la plante
            :return: Liste de commentaires
        """
        comments = self.db.table('comment').select("*").eq('planteID', plantID).order('id', desc=True).execute().data
        if len(comments) == 0:
            return []
        return comments

    def GetByID(self, commentID: int) -> Comment:
        """
            Récupère un commentaire par son ID
            :param commentID: ID du commentaire
            :return: Commentaire
        """
        comment = self.db.table('comment').select("*").eq('id', commentID).execute().data
        if len(comment) == 0:
            return None
        comment = comment[0]
        returnComment: Comment = Comment(comment["id"], comment["planteID"], self.userTable.GetByID(comment["authorID"]), comment["message"], comment["date"])
        returnComment.author.password = None
        returnComment.author.token = None
        return returnComment




    def Add(self, newComment: Comment) -> int:
        """
            Ajoute un commentaire à la base de données
            :param newComment: Commentaire à ajouter
            :return: commentID
        """
        self.db.table('comment').insert([{"planteID": newComment.planteID, "authorID": newComment.author.id, "message": newComment.message}]).execute()
        return self.db.table('comment').select("id").order('id', desc=True).limit(1).execute().data[0]["id"]

    def Delete(self, commentID: int):
        """
            Supprime un commentaire de la base de données
            :param commentID: ID du commentaire à supprimer
        """
        self.db.table('comment').delete().eq('id', commentID).execute()
        return