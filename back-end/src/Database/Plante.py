"""
    Gestion des requêtes de la table Plante
"""
from supabase import Client
import datetime

# Table utilisée pour les requêtes
from Database.User import UserTable
from Database.Comment import CommentTable

# Table utilisée pour le typage
from Database.Tables import Plante, SearchSettings, PlanteStatus


class PlanteTable:
    db: Client
    userTable: UserTable
    commentTable: CommentTable

    def __init__(self, db: Client, userTable: UserTable, commentTable: CommentTable):
        self.db = db
        self.userTable = userTable
        self.commentTable = commentTable
        return

    def GetByID(self, planteID: int) -> Plante:
        """
            Récupère une plante par son ID
            :param planteID: ID de la plante
            :return: Plante
        """
        plante = self.db.table('plante').select("*").eq('id', planteID).execute().data
        if len(plante) == 0:
            return None
        plante = plante[0]
        returnPlante = Plante(
            plante["id"], 
            self.userTable.GetByID(plante["ownerID"]) if plante["ownerID"] != None else None,
            self.userTable.GetByID(plante["guardianID"]) if plante["guardianID"] != None else None,
            plante["name"], 
            plante["description"], 
            plante["latitude"],
            plante["longitude"], 
            datetime.datetime.strptime(plante["date"], "%Y-%m-%d %H:%M:%S"),
            plante["statusID"]
        )
        if returnPlante.owner != None:
            returnPlante.owner.password = None
            returnPlante.owner.token = None
        if returnPlante.guardian != None:
            returnPlante.guardian.password = None
            returnPlante.guardian.token = None
        # Get all comments
        returnPlante.comments = self.commentTable.GetByPlanteID(returnPlante.id)
        return returnPlante

    def SearchAll(self, searchSettings: SearchSettings) -> list[Plante]:
        """
            Récupère toutes les plantes de la base de données
            :param searchSettings: Paramètres de recherche
            :return: Liste de plantes
        """
        plantes: list[Plante] = []
        allPlantes = self.db.table('plante').select("*").order("id", ascending=False).execute().data
        for plante in allPlantes:
            if (searchSettings.availablePlante and plante["statusID"] != PlanteStatus.DISPONIBLE) and (searchSettings.keptPlante and plante["statusID"] != PlanteStatus.GARDE) and (searchSettings.donePlante and plante["statusID"] != PlanteStatus.FINI):
                continue
            if searchSettings.ownerID != -1 and plante["ownerID"] != searchSettings.ownerID:
                continue
            if searchSettings.guardianID != -1 and plante["guardianID"] != searchSettings.guardianID:
                continue
            if searchSettings.latitude != -1 and searchSettings.longitude != -1 and searchSettings.radius != -1:
                if (searchSettings.latitude - searchSettings.radius) > plante["latitude"] or (searchSettings.latitude + searchSettings.radius) < plante["latitude"]:
                    continue
                if (searchSettings.longitude - searchSettings.radius) > plante["longitude"] or (searchSettings.longitude + searchSettings.radius) < plante["longitude"]:
                    continue
            plantes.append(self.GetByID(plante["id"]))
        return plantes



    def Add(self, newPlante: Plante) -> int:
        """
            Ajoute une plante à la base de données
            :param newPlante: Plante à ajouter
            :return: planteID
        """
        id = self.db.table('plante').insert([{
            "ownerID": newPlante.owner.id, 
            "name": newPlante.name, 
            "statusID": PlanteStatus.DISPONIBLE, 
            "latitude": newPlante.latitude, 
            "longitude": newPlante.longitude, 
            "picture": newPlante.picture 
        }]).execute().data[0]["id"]
        return id

    def Delete(self, plante: Plante) -> None:
        """
            Supprime une plante
            :param plante: Plante à supprimer
            :return: None
        """
        self.db.table('plante').delete().eq('id', plante.id).execute()
        return

    def Update(self, plante: Plante) -> None:
        """
            Met à jour la plante
            :param plante: Plante
            :return: None
        """
        self.db.table('plante').update({
            "ownerID": plante.owner.id if plante.owner != None else None,
            "guardianID": plante.guardian.id if plante.guardian != None else None,
            "name": plante.name,
            "statusID": plante.status,
            "latitude": plante.latitude,
            "longitude": plante.longitude,
            "picture": plante.picture
        }).eq('id', plante.id).execute()
        return
