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
POST /user/delete/{userID}
```
### Response
```json
200 OK (admin or user himself)
404 User not found
401 Unauthorized
```


# PLANTES
## Ajout d'une plante
### Request
```json
POST /plant/add
```
### Body
```json
{
  "plante": {
    "name": str,
    "latitude": float,
    "longitude": float
  },
  "token": {
    "accessToken": str
  }
}
```
### Response
```json
201 Created
{
    "plantID": int
}

401 Unauthorized
404 User not found
```

## Récupération de toute les plantes
### Request
```json
GET /plante/search
```
### Body
```json
{
    "searchSetting":{
        "availablePlante": bool,        // Si la plante est disponible
        "keptPlante": bool,             // Si la plante est gardée
        "donePlante": bool,             // Si la plante est terminée
        "ownerID": int,                 // ID du propriétaire (-1 = tous)
        "guardianID": int,              // ID du gardien (-1 = tous)
        "latitude": float,              // Latitude du centre de la zone de recherche (-1 = tous)
        "longitude": float,             // Longitude du centre de la zone de recherche (-1 = tous)
        "radius": float                 // Rayon de la zone de recherche (-1 = tous)
    },
    "token": {
        "accessToken": str
    }
}
```
### Response
```json
200 OK
[
    {
        "id": int,
        "owner":  {
            "id": int,
            "userTypeID": int,
            "pseudo": str,
        },
        "guardian": {
            "id": int,
            "userTypeID": int,
            "pseudo": str,
        },
        "name": str,
        "latitude": float,
        "longitude": float,
        "planteStatus": int {0=Disponible, 1=Gardée, 2=Terminée},
        "createdAt": datetime,
        "picture": BLOB
    },
    ...
]

401 Unauthorized
```

## Récupération des données d'une plante
### Request
```json
GET /plante/{plantID}
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
    "id": int,
    "ownerID": int,
    "guardianID": int,
    "name": str,
    "latitude": float,
    "longitude": float,
    "planteStatus": int {0=Disponible, 1=Gardée, 2=Terminée},
    "createdAt": datetime
}
```

## Supprimer une plante
### Request
```json
POST /plante/delete/{plantID}
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

401 Unauthorized (not owner or admin)
404 Plant not found
```

## Mettre à jours le gardien d'une plante

