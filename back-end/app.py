import json
from passlib.hash import sha256_crypt
from Database import *
import uvicorn

from fastapi import FastAPI, status, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
db: Database = Database("ARosaJe_Data.db")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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

@app.post("/user/delete/")
def DeleteUser(user: User, token: Token):
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
    if(not(requestUser.userTypeID == UserType.ADMIN) and not(requestUser.id == user.id)):# Si l'utilisateur n'est pas administrateur ET n'est pas l'utilisateur à supprimer
        return Response(status_code=401)

    user: User = db.UserGetByID(user.id)                             # Utilisateur à supprimer
    if(user == None):                                               # Si l'utilisateur n'existe pas
        return Response(status_code=404)
    db.UserDelete(user)
    return Response(status_code=200)

@app.post("/user/me", response_model=User)
def CurrentUser(token: Token):
    """
    Renvoie l'utilisateur connecté
    :param token: Token de l'utilisateur connecté
    :return: 200 si connecté, User
    :return: 401 si mauvais accessToken (ou introuvable)
    """
    if(token.accessToken == None):
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    user: User = db.UserGetByID(token.userID)
    del user.password
    del user.token
    return user
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

@app.post("/plante/", response_model=Plante)
def GetPlanteByID(plante: Plante, token: Token):
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

    plante: Plante = db.PlanteGetByID(plante.id)
    if(plante == None):                                             # Si la plante n'existe pas
        return Response(status_code=404)
    return plante

@app.post("/plante/delete/")
def DeletePlante(plante: Plante, token: Token):
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

    plante: Plante = db.PlanteGetByID(plante.id)                     # Plante à supprimer
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


##### CONVERSATION #####
@app.post("/conversation/", response_model=list[Conversation])
def GetConversations(token: Token):
    """
    Récupère les conversations d'un utilisateur
    :param token: Token de l'utilisateur
    :return: 200 Si connecté, conversations récupérées
    :return: 401 Si mauvais accessToken (ou introuvable)
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    conversations: list[Conversation] = db.ConversationGetByUserID(token.userID)
    return conversations
@app.post("/conversation/", response_model=list[int])
def GetConversationMessagesID(conversation: Conversation, token: Token):
    """
    Récupère les messages d'une conversation
    :param conversationID: ID de la conversation
    :return: 200 Si connecté, messages récupérés
    :return: 401 Si mauvais accessToken (ou introuvable), ou si l'utilisateur n'est pas administrateur ou si l'utilisateur n'est pas dans la conversation
    :return: 404 Si la conversation n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    conversation: Conversation = db.ConversationGetByID(conversation.id)
    if not(conversation.owner.id == token.userID or conversation.guardian.id == token.userID):
        return Response(status_code=401)                            # Si l'utilisateur n'est pas dans la conversation

    if(conversation == None):                                       # Si la conversation n'existe pas
        return Response(status_code=404)

    messagesID: list[int] = db.MessageIDsGetByConversationID(conversation.id)
    return messagesID
@app.post("/conversation/GetMessage/", response_model=PrivateMessage)
def GetConversationMessage(message: PrivateMessage, token: Token):
    """
    Récupère le contenu d'un message
    :param messageID: ID du message
    :return: 200 Si connecté, message récupéré
    :return: 401 Si mauvais accessToken (ou introuvable), ou si l'utilisateur n'est pas administrateur ou si l'utilisateur n'est pas dans la conversation
    :return: 404 Si le message n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    message: PrivateMessage = db.MessageGetByID(message.id)
    if not(message.conversation.owner.id == token.userID or message.conversation.guardian.id == token.userID):
        return Response(status_code=401)                            # Si l'utilisateur n'est pas dans la conversation

    if(message == None):                                            # Si le message n'existe pas
        return Response(status_code=404)

    return message


@app.post("/conversation/add/")
def AddConversation(conversation: Conversation, token: Token):
    """
    Ajoute une conversation
    :param conversation: Conversation à ajouter
    :return: 201 Si connecté, conversation ajoutée
    :return: 400 Si mauvais paramètres (owner et guardian identiques)
    :return: 401 Si mauvais accessToken (ou introuvable)
    :return: 404 Si l'utilisateur n'existe pas
    :return: 409 Si la conversation existe déjà
    """
    if(conversation.owner.id == conversation.guardian.id):          # Si l'utilisateur est son propre gardien
        return Response(status_code=400)

    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    if(db.UserGetByID(conversation.owner.id) == None or db.UserGetByID(conversation.guardian.id) == None):
        return Response(status_code=404)

    if(db.ConversationGetByUsersID(conversation.owner.id, conversation.guardian.id) != None):
        return Response(status_code=409)

    conversationID: int = db.ConversationAdd(conversation)
    returnData: dict = {"conversationID": conversationID}
    return Response(status_code=201, content=json.dumps(returnData), media_type="application/json")
@app.post("/conversation/{conversationID}/add/")
def AddConversationMessage(conversationID: int, message: PrivateMessage, token: Token):
    """
    Ajoute un message à une conversation
    :param conversationID: ID de la conversation
    :param message: Message à ajouter
    :return: 201 Si connecté, message ajouté
    :return: 400 Si mauvais paramètres (message et image None)
    :return: 401 Si mauvais accessToken (ou introuvable), ou si l'utilisateur n'est pas administrateur ou si l'utilisateur n'est pas dans la conversation
    :return: 404 Si la conversation n'existe pas
    """
    if(message.message == None and message.picture == None):           # Si le message est vide
        return Response(status_code=400)

    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    conversation: Conversation = db.ConversationGetByID(conversationID)
    if(conversation == None):                                       # Si la conversation n'existe pas
        return Response(status_code=404)
    if not(conversation.owner.id == token.userID or conversation.guardian.id == token.userID):
        return Response(status_code=401)                            # Si l'utilisateur n'est pas dans la conversation


    message.conversation = conversation
    message.sender = db.UserGetByID(token.userID)
    messageID: int = db.MessageAdd(message)
    returnData: dict = {"messageID": messageID}
    return Response(status_code=201, content=json.dumps(returnData), media_type="application/json")
########################

##### COMMENTS #####
@app.post("/commentaire/", response_model=list[Comment])
def GetComments(plante: Plante, token: Token):
    """
    Récupère les commentaires d'une plante
    :return: 200 Si connecté, commentaires récupérés
    :return: 401 Si mauvais accessToken (ou introuvable)
    :return: 404 Si la plante n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    plante: Plante = db.PlanteGetByID(plante.id)
    if(plante == None):                                             # Si la plante n'existe pas
        return Response(status_code=404)

    comments: list[Comment] = db.CommentGetByPlanteID(plante.id)
    return comments

@app.post("/commentaire/{planteID}/add/")
def AddComment(planteID: int, comment: Comment, token: Token):
    """
    Ajoute un commentaire à une plante
    :param plantID: ID de la plante
    :param comment: Commentaire à ajouter
    :return: 201 Si connecté, commentaire ajouté
    :return: 400 Si mauvais paramètres (message None)
    :return: 401 Si mauvais accessToken (ou introuvable)
    :return: 404 Si la plante n'existe pas
    """
    if(comment.message == None):                                    # Si le commentaire est vide
        return Response(status_code=400)

    if(token== None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    plante: Plante = db.PlanteGetByID(planteID)
    if(plante == None):                                             # Si la plante n'existe pas
        return Response(status_code=404)

    comment.plante = plante
    comment.author = db.UserGetByID(token.userID)
    commentID: int = db.CommentAdd(comment)
    returnData: dict = {"commentID": commentID}
    return Response(status_code=201, content=json.dumps(returnData), media_type="application/json")

@app.post("/commentaire/delete/")
def DeleteComment(comment: Comment, token: Token):
    """
    Supprime un commentaire
    :return: 200 Si connecté, commentaire supprimé
    :return: 401 Si mauvais accessToken (ou introuvable)
    :return: 404 Si le commentaire n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(db.TokenGetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = db.TokenGetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    comment: Comment = db.CommentGetByID(comment.id)
    if(comment == None):                                            # Si le commentaire n'existe pas
        return Response(status_code=404)

    if not(comment.author.id == token.userID):                      # Si l'utilisateur n'est pas l'auteur du commentaire
        return Response(status_code=401)

    db.CommentDelete(comment.id)
    return Response(status_code=200)
####################

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1')