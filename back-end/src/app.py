import json
from passlib.hash import sha256_crypt
import uvicorn
import datetime
from fastapi import FastAPI, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse

from Database import tokenTable, userTable, commentTable, planteTable, conversationTable, privateMessageTable
from Database.Tables import User, Comment, Plante, Conversation, PrivateMessage, Token, PlanteStatus, UserType, SearchSettings, SearchSettingsUser

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://arosaje.ibsolutions.cloud", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
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
    newUser.pseudo = newUser.pseudo.strip()
    newUser.password = newUser.password.strip()
    if(userTable.GetByPseudo(newUser.pseudo) != None):
        return Response(status_code=409)
    newUser.password = sha256_crypt.encrypt(newUser.password)
    userTable.Add(newUser)
    return Response(status_code=201)

@app.post("/user/login", response_model=Token)
def Login(loginUser: User):
    """
    Connecte un utilisateur
    :param user: Utilisateur à connecter
    :return: 200 si connecté, {accessToken: "accessToken", refreshToken: "refreshToken"}
    :return: 401 si mauvais pseudo 
    :return: 402 mot de passe
    """
    loginUser.pseudo = loginUser.pseudo.strip()
    loginUser.password = loginUser.password.strip()
    user = userTable.GetByPseudo(loginUser.pseudo)
    if(user == None):                                            # Si le pseudo n'existe pas
        return Response(status_code=401)
    if(not sha256_crypt.verify(loginUser.password, user.password)):   # Si le mot de passe est incorrect
        return Response(status_code=402)
    newToken: Token = tokenTable.Generate(user)
    newToken.userTypeID = user.userTypeID
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
    if(tokenTable.GetByRefreshToken(token.refreshToken) == None):
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    token: Token = tokenTable.Refresh(tokenTable.GetByRefreshToken(token.refreshToken))
    return token
    
@app.post("/user/logout")
def Logout(userID: dict):
    """
    Déconnecte un utilisateur
    :param user: Utilisateur à déconnecter
    :return: 200 si déconnecté
    """
    tokenTable.Delete(userTable.GetByID(userID["userID"]))
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    user: User = userTable.GetByID(userID)
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
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token == None):                                              # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    requestUser: User = userTable.GetByID(token.userID)                # Utilisateur qui fait la requête
    if(not(requestUser.userTypeID == UserType.ADMIN) and not(requestUser.id == user.id)):# Si l'utilisateur n'est pas administrateur ET n'est pas l'utilisateur à supprimer
        return Response(status_code=401)

    user: User = userTable.GetByID(user.id)                             # Utilisateur à supprimer
    if(user == None):                                               # Si l'utilisateur n'existe pas
        return Response(status_code=404)
    userTable.Delete(user)
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    user: User = userTable.GetByID(token.userID)
    del user.password
    del user.token
    return user

@app.post("/user/Search", response_model=list[User])
def SearchUser(search: SearchSettingsUser, token: Token):
    """
    Recherche d'une liste d'utilisateurs
    :param search: Paramètres de recherche
    :return: 200 si connecté, [User]
    :return: 401 si mauvais accessToken (ou introuvable)
    """
    if(token.accessToken == None):
        return Response(status_code=401)
    if(tokenTable.GetByAccessToken(token.accessToken) == None):
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    users: list[User] = userTable.Search(search)
    for user in users:
        del user.password
        del user.token
    return users
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)

    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    requestUser: User = userTable.GetByID(token.userID) # Utilisateur qui fait la requête
    if(requestUser == None):                                        # Si l'utilisateur n'existe pas
        return Response(status_code=404)

    plante.owner = requestUser
    planteID: int = planteTable.Add(plante)

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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)
    plantes: list[Plante] = planteTable.SearchAll(searchSetting)
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    plante: Plante = planteTable.GetByID(plante.id)
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
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token == None):                                              # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    plante: Plante = planteTable.GetByID(plante.id)                     # Plante à supprimer
    if(plante == None):                                             # Si la plante n'existe pas
        return Response(status_code=404)

    requestUser: User = userTable.GetByID(token.userID)                # Utilisateur qui fait la requête
    if(not(requestUser.userTypeID == UserType.ADMIN) and not(requestUser.id == plante.owner.id)):# Si l'utilisateur n'est pas administrateur ET n'est pas l'utilisateur à supprimer
        return Response(status_code=401)

    planteTable.Delete(plante)
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    planteToUpdate: Plante = planteTable.GetByID(plante.id)            # Plante à mettre à jour
    if(planteToUpdate == None):                                     # Si la plante n'existe pas
        return Response(status_code=404)
    requestUser: User = userTable.GetByID(token.userID)                # Utilisateur qui fait la requête
    if(requestUser.userTypeID != UserType.ADMIN and requestUser.id != planteToUpdate.owner.id and requestUser.id != planteToUpdate.guardian.id):
        return Response(status_code=401)                            # Si l'utilisateur n'est pas administrateur ET n'est pas l'utilisateur de la plante

    planteToUpdate.status = plante.status
    planteTable.Update(planteToUpdate)
    return Response(status_code=200)

@app.post("/plante/updateGuardian/")
def UpdatePlanteGuardian(plante: Plante, token: Token):
    """
    Met à jour le gardien d'une plante
    :param plante: Plante à mettre à jour
    :return: 200 Si connecté et administrateur/proprietaire, plante mise à jour
    :return: 401 Si mauvais accessToken (ou introuvable) ou si l'utilisateur n'est pas administrateur ou si l'utilisateur n'est pas l'un guardien de la plante ou (si l'utilisateur est un gardien ET que la plante est déjà gardé)
    :return: 404 Si la plante n'existe pas
    """
    if(token.accessToken == None):                                  # Si l'accessToken n'est pas présent
        return Response(status_code=401)
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    planteToUpdate: Plante = planteTable.GetByID(plante.id)            # Plante à mettre à jour
    if(planteToUpdate == None):                                     # Si la plante n'existe pas
        return Response(status_code=404)
    requestUser: User = userTable.GetByID(token.userID)                # Utilisateur qui fait la requête
    if(requestUser.userTypeID != UserType.GARDIEN and requestUser.userTypeID != UserType.ADMIN):        # Si l'utilisateur est ni gardien ni administrateur
        return Response(status_code=401)
    if(requestUser.userTypeID == UserType.GARDIEN and planteToUpdate.guardian != None and not(requestUser.id == planteToUpdate.owner.id)):# Si l'utilisateur est gardien ET que la plante est déjà gardé ET que l'utilisateur n'est pas le propriétaire de la plante
        return Response(status_code=401)
    

    planteToUpdate.guardian = plante.guardian
    planteTable.Update(planteToUpdate)
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    conversations: list[Conversation] = conversationTable.GetByUserID(token.userID)
    return conversations
@app.post("/conversation/Get/", response_model=list[PrivateMessage])
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    conversation: Conversation = conversationTable.GetByID(conversation.id)
    if(conversation == None):                                       # Si la conversation n'existe pas
        return Response(status_code=404)
    if not(conversation.owner.id == token.userID or conversation.guardian.id == token.userID):
        return Response(status_code=401)                            # Si l'utilisateur n'est pas dans la conversation


    messagesID: list[int] = privateMessageTable.MessageIDsGetByConversationID(conversation.id)
    messages: list[PrivateMessage] = []
    for messageID in messagesID:
        messages.append(privateMessageTable.GetByID(messageID))
    return messages
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    message: PrivateMessage = privateMessageTable.GetByID(message.id)
    if(message == None):                                            # Si le message n'existe pas
        return Response(status_code=404)
    if not(message.conversation.owner.id == token.userID or message.conversation.guardian.id == token.userID):
        return Response(status_code=401)                            # Si l'utilisateur n'est pas dans la conversation


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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    if(userTable.GetByID(conversation.owner.id) == None or userTable.GetByID(conversation.guardian.id) == None):
        return Response(status_code=404)

    if(conversationTable.GetByUsersID(conversation.owner.id, conversation.guardian.id) != None):
        return Response(status_code=409)

    conversationID: int = conversationTable.Add(conversation)
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    conversation: Conversation = conversationTable.GetByID(conversationID)
    if(conversation == None):                                       # Si la conversation n'existe pas
        return Response(status_code=404)
    if not(conversation.owner.id == token.userID or conversation.guardian.id == token.userID):
        return Response(status_code=401)                            # Si l'utilisateur n'est pas dans la conversation


    message.conversation = conversation
    message.sender = userTable.GetByID(token.userID)
    messageID: int = privateMessageTable.Add(message)
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    plante: Plante = planteTable.GetByID(plante.id)
    if(plante == None):                                             # Si la plante n'existe pas
        return Response(status_code=404)

    comments: list[Comment] = commentTable.GetByPlanteID(plante.id)
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    plante: Plante = planteTable.GetByID(planteID)
    if(plante == None):                                             # Si la plante n'existe pas
        return Response(status_code=404)

    comment.planteID = planteID
    comment.author = userTable.GetByID(token.userID)
    commentID: int = commentTable.Add(comment)
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
    if(tokenTable.GetByAccessToken(token.accessToken) == None):        # Si l'accessToken n'existe pas
        return Response(status_code=401)
    token: Token = tokenTable.GetByAccessToken(token.accessToken)
    if(token.expire < datetime.datetime.now()):                     # Si l'accessToken est expiré
        return Response(status_code=401)

    comment: Comment = commentTable.GetByID(comment.id)
    if(comment == None):                                            # Si le commentaire n'existe pas
        return Response(status_code=404)

    if not(comment.author.id == token.userID):                      # Si l'utilisateur n'est pas l'auteur du commentaire
        return Response(status_code=401)

    commentTable.Delete(comment.id)
    return Response(status_code=200)
####################


##### FILES #####
@app.get("/file/CGU/")
def GetCGU():
    """
    Récupère les CGU
    :return: 200 Si connecté, CGU récupérées
    """
    return FileResponse("files/CGU.pdf", media_type="application/pdf")
@app.get("/file/rgpd/")
def GetTraitement():
    """
    Récupère le carnet de traitement
    :return: 200 Si connecté, Carnet de traitement récupérées
    """
    return FileResponse("files/Carnet de traitement.pdf", media_type="application/pdf")


# Route pour gérer les requêtes OPTIONS
@app.options("/user/register")
@app.options("/user/login")
@app.options("/user/refreshToken")
@app.options("/user/logout")
@app.options("/user/get/{userID}")
@app.options("/user/delete/")
@app.options("/user/me")
@app.options("/user/Search")
@app.options("/plante/add")
@app.options("/plante/search")
@app.options("/plante/")
@app.options("/plante/delete/")
@app.options("/plante/updateStatus/")
@app.options("/plante/updateGuardian/")
@app.options("/conversation/")
@app.options("/conversation/Get/")
@app.options("/conversation/GetMessage/")
@app.options("/conversation/add/")
@app.options("/conversation/{conversationID}/add/")
@app.options("/commentaire/")
@app.options("/commentaire/{planteID}/add/")
@app.options("/commentaire/delete/")
@app.options("/file/CGU/")
@app.options("/file/rgpd/")
def options():
    response = JSONResponse(content={})
    response.headers["Access-Control-Allow-Origin"] = "https://arosaje.ibsolutions.cloud"
    response.headers["Access-Control-Allow-Methods"] = ["GET", "POST", "OPTIONS"]
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=1418)