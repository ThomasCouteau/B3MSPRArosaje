import requests

URL: str = "http://localhost:1418"
USERTYPE_BOTANISTE: int = 1
USERTYPE_ADMIN: int = 2
USERTYPE_GARDIENT: int = 3


def test_fonctionnel():
    """
        Test fonctionnel
    """
    # Création d'un compte gardient
    Register("gardient", "gardient")
    
    # Connexion de l'utilisateur
    tokens_gardient_1 = Login("gardient", "gardient")

    # Création d'un poste
    planteID = AddPlante(tokens_gardient_1["accessToken"], "plante", 0.0, 0.0)

    # Création d'un compte gardient
    Register("gardient2", "gardient2")

    # Connexion de l'utilisateur
    tokens_gardient_2 = Login("gardient2", "gardient2")

    # Garder la plante
    GarderPlante(tokens_gardient_2["accessToken"], planteID, tokens_gardient_2["userID"])

    # Envoi d'un message vers le premier gardient
    conversationID = CreateConversation(tokens_gardient_2["accessToken"], tokens_gardient_2["userID"], tokens_gardient_1["userID"])
    SendMessage(tokens_gardient_2["accessToken"], conversationID, "message")

    # Depuis le premier gardient récupération du message
    message = GetMessage(tokens_gardient_1["accessToken"], conversationID)

    # Création d'un compte Botaniste
    Register("botaniste", "botaniste")

    # Connexion de l'utilisateur
    tokens_botaniste = Login("botaniste", "botaniste")

    # Envoi d'un commentaire sur le poste
    SendComment(tokens_botaniste["accessToken"], planteID, "commentaire")

    # Depuis le premier gardient récupération du commentaire
    comment = GetComment(tokens_gardient_1["accessToken"], planteID)

    # Nettoyage de la base de données
    CleanDatabase()



# 1	Création d'un compte gardient 	Méthode POST sur l’api créer un compte	Utilisateur créé
# 2	Connexion de l'utilisateur	Méthode POST sur l’api pour la connexion	Récupération du token d'accès
# 3	Création d'un poste	Méthode POST sur l'api pour créer un poste	Poste créé
# 4	Création d'un compte gardient 	Méthode POST sur l’api créer un compte	Utilisateur créé
# 5	Connexion de l'utilisateur	Méthode POST sur l’api pour la connexion	Récupération du token d'accès
# 6	Garder la plante	Méthode POST sur l'api pour garder la plante	Plante gardé
# 7	Envoi d'un message vers le premier gardient	Méthode POST sur l'api pour envoyer un message	Message envoyé
# 8	Depuis le premier gardient récupération du message	Méthode POST sur l'api pour récupérer le message	Message reçus
# 9	Création d'un compte Botaniste 	Méthode POST sur l’api créer un compte	Utilisateur créé
# 10	Connexion de l'utilisateur	Méthode POST sur l’api pour la connexion	Récupération du token d'accès
# 11	Envoi d'un commentaire sur le poste	Méthode POST sur l’api pour envoyer un commentaire	Commentaire créé
# 12	Depuis le premier gardient récupération du commentaire	Méthode POST sur l'api pour récupérer le commentaire	Commentaire visible
# 13	Nettoyage de la base de données		

def Register(userTypeID: int, pseudo: str, password: str) -> None:
    """
        Création d'un compte
    """
    response = requests.post(
        f"{URL}/user/register",
        json={
            "userTypeID": userTypeID,
            "pseudo": pseudo,
            "password": password
        }
    )
    assert response.status_code == 201
    return
def Login(pseudo: str, password: str) -> str:
    """
        Connexion de l'utilisateur
    """
    response = requests.post(
        f"{URL}/user/login",
        json={
            "pseudo": pseudo,
            "password": password
        }
    )
    assert response.status_code == 200
    assert response.json()["accessToken"] != None
    assert response.json()["refreshToken"] != None
    return response.json()


def AddPlante(accessToken: str, name: str, latitude: float, longitude: float) -> int:
    """
        Ajout d'une plante
    """
    response = requests.post(
        f"{URL}/plant/add",
        json={
            "plante": { 
                "name": name,
                "latitude": latitude,
                "longitude": longitude
            },
            "token": {
                "accessToken": accessToken
            }
        }
    )
    assert response.status_code == 201
    assert response.json()["plantID"] != None
    return response.json()["plantID"]
def GarderPlante(accessToken: str, plantID: int, guardianID: int) -> None:
    """
        Garder une plante
    """
    response = requests.post(
        f"{URL}/plant/updateGuardian",
        json={
            "plante":{
                "id": plantID,
                "guardian": {
                    "id": guardianID
                }
            },
            "token": {
                "accessToken": accessToken
            }
        }
    )
    assert response.status_code == 200
    return

def CreateConversation(accessToken: str, ownerID: int, guardianID: int) -> int:
    """
        Création d'une conversation
    """
    response = requests.post(
        f"{URL}/conversation/add",
        json={
            "conversation": {
                "owner": {
                    "id": ownerID
                },
                "guardian": {
                    "id": guardianID
                }
            },
            "token": {
                "accessToken": accessToken
            }
        }
    )
    assert response.status_code == 201
    assert response.json()["conversationID"] != None
    return response.json()["conversationID"]
def SendMessage(accessToken: str, message: str) -> None:
    """
        Envoi d'un message
    """
    response = requests.post(
        f"{URL}/message/add",
        json={
            "message": {
                "message": message
            },
            "token": {
                "accessToken": accessToken
            }
        }
    )
    assert response.status_code == 201
    assert response.json()["messageID"] != None
    return
def GetMessage(accessToken: str, conversationID: int) -> str:
    """
        Récupération d'un message
    """
    response = requests.post(
        f"{URL}/message/GetMessage",
        json={
            "conversationID": conversationID,
            "token": {
                "accessToken": accessToken
            }
        }
    )
    assert response.status_code == 200
    assert response.json() != None
    return response.json()[0]

def SendComment(accessToken: str, plantID: int, comment: str) -> None:
    response = requests.post(
        f"{URL}/commentaire/"+str(plantID)+"/add",
        json={
            "comment": {
                "message": comment
            },
            "token": {
                "accessToken": accessToken
            }
        }
    )
    assert response.status_code == 201
    assert response.json()["commentID"] != None
    return
def GetComment(accessToken: str, plantID: int) -> str:
    response = requests.post(
        f"{URL}/commentaire/",
        json={
            "plantID": plantID,
            "token": {
                "accessToken": accessToken
            }
        }
    )
    assert response.status_code == 200
    assert response.json() != None
    return response.json()[0]

def CleanDatabase(guardian_1, guardiant_2, botaniste):
    """
        Nettoyage de la base de données
    """
    response = requests.post(
        f"{URL}/user/delete",
        json={
            "user": {
                "id": guardian_1
            }
        }
    )
    assert response.status_code == 200
    response = requests.post(
        f"{URL}/user/delete",
        json={
            "user": {
                "id": guardiant_2
            }
        }
    )
    assert response.status_code == 200
    response = requests.post(
        f"{URL}/user/delete",
        json={
            "user": {
                "id": botaniste
            }
        }
    )
    assert response.status_code == 200
    return
