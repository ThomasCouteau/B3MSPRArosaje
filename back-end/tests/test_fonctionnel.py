import requests

URL: str = "http://localhost:1418"

def Register(username: str, password: str) -> str:
    """
        Création d'un compte
    """
    response = requests.post(
        f"{URL}/register",
        json={
            "username": username,
            "password": password
        }
    )
    return response.json()["token"]

def test_fonctionnel():
    """
        Test fonctionnel
    """
    # Création d'un compte gardient

    
    # Connexion de l'utilisateur

    # Création d'un poste

    # Création d'un compte gardient

    # Connexion de l'utilisateur

    # Garder la plante

    # Envoi d'un message vers le premier gardient

    # Depuis le premier gardient récupération du message

    # Création d'un compte Botaniste

    # Connexion de l'utilisateur

    # Envoi d'un commentaire sur le poste

    # Depuis le premier gardient récupération du commentaire

    # Nettoyage de la base de données



1	Création d'un compte gardient 	Méthode POST sur l’api créer un compte	Utilisateur créé
2	Connexion de l'utilisateur	Méthode POST sur l’api pour la connexion	Récupération du token d'accès
3	Création d'un poste	Méthode POST sur l'api pour créer un poste	Poste créé
4	Création d'un compte gardient 	Méthode POST sur l’api créer un compte	Utilisateur créé
5	Connexion de l'utilisateur	Méthode POST sur l’api pour la connexion	Récupération du token d'accès
6	Garder la plante	Méthode POST sur l'api pour garder la plante	Plante gardé
7	Envoi d'un message vers le premier gardient	Méthode POST sur l'api pour envoyer un message	Message envoyé
8	Depuis le premier gardient récupération du message	Méthode POST sur l'api pour récupérer le message	Message reçus
9	Création d'un compte Botaniste 	Méthode POST sur l’api créer un compte	Utilisateur créé
10	Connexion de l'utilisateur	Méthode POST sur l’api pour la connexion	Récupération du token d'accès
11	Envoi d'un commentaire sur le poste	Méthode POST sur l’api pour envoyer un commentaire	Commentaire créé
12	Depuis le premier gardient récupération du commentaire	Méthode POST sur l'api pour récupérer le commentaire	Commentaire visible
13	Nettoyage de la base de données		
