from flask import Flask, request, Response
import json
from Database import *

app = Flask(__name__)

db: Database = Database("database.db")

@app.route('/')
def hello_world():
    return 'Hello, World!'

##### AUTH #####
@app.post("/user/")
def AddUser(newUser: User):
    """
    Ajoute un utilisateur à la base de données
    :param newUser: Utilisateur à ajouter
    :return: 201 si ajouté
    :return: 409 si le pseudo déjà présent
    """
    if(db.UserGetByPseudo(newUser.pseudo) != None):
        return Response(status_code=409)
    db.UserAdd(newUser)
    return Response(status_code=201)
################





# @app.post("/user/")
# async def add_usere(newUser: Article):
#     """
#     Ajoute un article à la base de données
#     :param newArticle: Article à ajouter
#     :return: 201 si ajouté, 409 si ID déjà présent    
#     """
#     if(db.ArticleGetByID(newArticle.id) != None):
#         return Response(status_code=status.HTTP_409_CONFLICT)
#     db.ArticleAdd(newArticle)
#     return Response(status_code=status.HTTP_201_CREATED)


if __name__ == '__main__':
    app.secret_key = '2d9-E2.)f&é,A$p@fpa+zSU03êû9_'
    # app.run(debug=False)
    app.run(debug=True)