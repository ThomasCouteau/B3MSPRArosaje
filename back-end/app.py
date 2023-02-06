import json
from passlib.hash import sha256_crypt
from Database import *
import uvicorn

from fastapi import FastAPI, status, Response

app = FastAPI()
db: Database = Database("ARosaJe_Data.db")


##### AUTH #####
@app.post("/user/register")
def Register(newUser: User):
    """
    Ajoute un utilisateur à la base de données
    :param newUser: Utilisateur à ajouter
    :return: 201 si ajouté
    :return: 409 si le pseudo déjà présent
    """
    if(db.UserGetByPseudo(newUser.pseudo) != None):
        return Response(status_code=409)
    newUser.password = sha256_crypt.encrypt(newUser.password)
    db.UserAdd(newUser)
    return Response(status_code=201)

@app.post("/user/login", response_model=Token)
def Login(user: User):
    """
    Connecte un utilisateur
    :param user: Utilisateur à connecter
    :return: 200 si connecté, {accessToken: "accessToken", refreshToken: "refreshToken"}
    :return: 401 si mauvais pseudo ou mot de passe
    """
    if(db.UserGetByPseudo(user.pseudo) == None):                                            # Si le pseudo n'existe pas
        return Response(status_code=401)
    if(not sha256_crypt.verify(user.password, db.UserGetByPseudo(user.pseudo).password)):   # Si le mot de passe est incorrect
        return Response(status_code=401)
    newToken: Token = db.TokenGenerate(db.UserGetByPseudo(user.pseudo))
    return newToken

@app.post("/user/refreshToken", response_model=Token)
def RefreshToken(token: Token):
    """
    Renvoie un nouveau accessToken
    :param user: Utilisateur à connecter
    :return: 200 si connecté, {accessToken: "accessToken"}
    :return: 401 si mauvais refreshToken (ou introuvable)
    """
    if(token.refreshToken == None):
        return Response(status_code=401)
    if(db.TokenGetByRefreshToken(token.refreshToken) == None):
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    token: Token = db.TokenRefresh(db.TokenGetByRefreshToken(token.refreshToken))
    return token
    
@app.post("/user/logout")
def Logout(userID: dict):
    """
    Déconnecte un utilisateur
    :param user: Utilisateur à déconnecter
    :return: 200 si déconnecté
    """
    db.TokenDelete(db.UserGetByID(userID["userID"]))
    return Response(status_code=200)

@app.post("/user/get/{userID}", response_model=User)
def GetUser(userID: int, token: Token):
    """
    Renvoie un utilisateur
    :param userID: ID de l'utilisateur à renvoyer
    :return: 200 si connecté, User
    :return: 401 si mauvais accessToken (ou introuvable)
    :return: 404 si l'utilisateur n'existe pas
    """
    if(token.accessToken == None):
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    user: User = db.UserGetByID(userID)
    if(user == None):
        return Response(status_code=404)
    del user.password
    del user.token
    return user

@app.post("/user/delete/{userID}")
def DeleteUser(userID: int, token: Token):
    """
    Supprime un utilisateur
    :param userID: ID de l'utilisateur à supprimer
    :return: 200 si connecté et administrateur
    :return: 401 si mauvais accessToken (ou introuvable) ou si l'utilisateur n'est pas administrateur
    :return: 404 si l'utilisateur n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token == None):                                              # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    requestUser: User = db.UserGetByID(token.userID)                # Utilisateur qui fait la requête
    if(not(requestUser.userTypeID == UserType.ADMIN) and not(requestUser.id == userID)):# Si l'utilisateur n'est pas administrateur ET n'est pas l'utilisateur à supprimer
        return Response(status_code=401)

    user: User = db.UserGetByID(userID)                             # Utilisateur à supprimer
    if(user == None):                                               # Si l'utilisateur n'existe pas
        return Response(status_code=404)
    db.UserDelete(user)
    return Response(status_code=200)
################



##### PLANTE #####
@app.post("/plante/add")
def AddPlante(plante: Plante, token: Token):
    """
    Ajoute une plante à la base de données
    :param plante: Plante à ajouter
    :return: 201 si ajouté
    :return: 401 si mauvais accessToken (ou introuvable)
    :return: 404 si l'utilisateur n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)

    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    requestUser: User = db.UserGetByID(token.userID) # Utilisateur qui fait la requête
    if(requestUser == None):                                        # Si l'utilisateur n'existe pas
        return Response(status_code=404)

    plante.owner = requestUser
    planteID: int = db.PlanteAdd(plante)

    returnData: dict = {"planteID": planteID}
    return Response(status_code=201, content=json.dumps(returnData), media_type="application/json")

@app.post("/plante/search", response_model=list[Plante])
def GetPlanteAll(searchSetting: SearchSettings, token: Token):
    """
    Renvoie toutes les plantes
    :return: 200 si connecté, liste de plantes
    :return: 401 si mauvais accessToken (ou introuvable)
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)
    plantes: list[Plante] = db.PlanteSearchAll(searchSetting)
    return plantes

@app.post("/plante/{planteID}", response_model=Plante)
def GetPlanteByID(planteID: int, token: Token):
    """
    Renvoie une plante
    :param planteID: ID de la plante à renvoyer
    :return: 200 si connecté, plante
    :return: 401 si mauvais accessToken (ou introuvable)
    :return: 404 si la plante n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    plante: Plante = db.PlanteGetByID(planteID)
    if(plante == None):                                             # Si la plante n'existe pas
        return Response(status_code=404)
    return plante

@app.post("/plante/delete/{planteID}")
def DeletePlante(planteID: int, token: Token):
    """
    Supprime une plante
    :param planteID: ID de la plante à supprimer
    :return: 200 si connecté et administrateur
    :return: 401 si mauvais accessToken (ou introuvable) ou si l'utilisateur n'est pas administrateur
    :return: 404 si la plante n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token == None):                                              # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    plante: Plante = db.PlanteGetByID(planteID)                     # Plante à supprimer
    if(plante == None):                                             # Si la plante n'existe pas
        return Response(status_code=404)

    requestUser: User = db.UserGetByID(token.userID)                # Utilisateur qui fait la requête
    if(not(requestUser.userTypeID == UserType.ADMIN) and not(requestUser.id == plante.owner.id)):# Si l'utilisateur n'est pas administrateur ET n'est pas l'utilisateur à supprimer
        return Response(status_code=401)

    db.PlanteDelete(plante)
    return Response(status_code=200)

@app.post("/plante/updateStatus/")
def UpdatePlanteStatus(plante: Plante, token: Token):
    """
    Met à jour le status d'une plante
    :param plante: Plante à mettre à jour
    :return: 200 Si connecté et administrateur/proprietaire, plante mise à jour
    :return: 401 Si mauvais accessToken (ou introuvable) ou si l'utilisateur n'est pas administrateur ou si l'utilisateur n'est pas l'utilisateur de la plante
    :return: 404 Si la plante n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    planteToUpdate: Plante = db.PlanteGetByID(plante.id)            # Plante à mettre à jour
    if(planteToUpdate == None):                                     # Si la plante n'existe pas
        return Response(status_code=404)
    requestUser: User = db.UserGetByID(token.userID)                # Utilisateur qui fait la requête
    if(not(requestUser.userTypeID == UserType.ADMIN) and not(requestUser.id == planteToUpdate.owner.id)):
        return Response(status_code=401)                            # Si l'utilisateur n'est pas administrateur ET n'est pas l'utilisateur de la plante

    planteToUpdate.status = plante.status
    db.PlanteUpdate(planteToUpdate)
    return Response(status_code=200)

@app.post("/plante/updateGuardian/")
def UpdatePlanteGuardian(plante: Plante, token: Token):
    """
    Met à jour le gardien d'une plante
    :param plante: Plante à mettre à jour
    :return: 200 Si connecté et administrateur/proprietaire, plante mise à jour
    :return: 401 Si mauvais accessToken (ou introuvable) ou si l'utilisateur n'est pas administrateur ou si l'utilisateur n'est pas l'utilisateur de la plante
    :return: 404 Si la plante n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    planteToUpdate: Plante = db.PlanteGetByID(plante.id)            # Plante à mettre à jour
    if(planteToUpdate == None):                                     # Si la plante n'existe pas
        return Response(status_code=404)
    requestUser: User = db.UserGetByID(token.userID)                # Utilisateur qui fait la requête
    if(not(requestUser.userTypeID == UserType.ADMIN) and not(requestUser.id == planteToUpdate.owner.id)):
        return Response(status_code=401)                            # Si l'utilisateur n'est pas administrateur ET n'est pas l'utilisateur de la plante

    planteToUpdate.guardian = plante.guardian
    db.PlanteUpdate(planteToUpdate)
    return Response(status_code=200)


##################



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1')