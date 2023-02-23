"""
    Liste des tables de la base de données
"""
from dataclasses import dataclass
from typing import Union
import datetime



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
    userTypeID: Union[UserType, int, None] = None

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