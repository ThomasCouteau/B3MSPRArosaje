# B3MSPRArosaje

# AUTHENTIFICATION
## Creation utilisateur
### Request
```
POST /user/register
```
### Body
```json
{
    "userTypeID": int{1=Botaniste, 2=Admin, 3=Gardien},
    "pseudo": str,
    "password": str
}
```
### Response
```json
201 Created
409 Pseudo already exists
```

## Connexion utilisateur
### Request
```
POST /user/login
```
### Body
```json
{
    "pseudo": str,
    "password": str
}
```
### Response
```json
200 OK
{
    "accessToken": str,
    "refreshToken": str
}

401 Unauthorized
```

## Regénération du token d'accès
### Request
```
POST /user/refreshToken
```
### Body
```json
{
    "refreshToken": str
}
```
## Response
```json
200 OK
{
    "accessToken": str,
    "refreshToken": str
}

401 Mauvais refreshToken ou introuvable
```

## Déconnexion utilisateur
### Request
```
POST /user/logout
```
### Body
```json
{
    "userID": int
}
```
### Response
```json
200 OK
```

## Récupération des données d'un utilisateur
### Request
```json
GET /user/{userID}
```
### Body
```json
{
    "accessToken": str
}
```
### Response
```json
200 OK
{
    "userID": int,
    "userTypeID": int{1=Botaniste, 2=Admin, 3=Gardien},
    "pseudo": str,
}

404 User not found
401 Unauthorized
```

## Suppression d'un utilisateur
### Request
```json
DELETE /user/{userID}
```
### Response
```json
200 OK (admin or user himself)
404 User not found
401 Unauthorized
```
