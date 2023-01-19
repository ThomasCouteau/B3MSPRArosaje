# B3MSPRArosaje

# Creation utilisateur
## Request
```
POST /user/
```
## Body
```json
{
    "userTypeID": int{1=Botaniste, 2=Admin, 3=Gardien},
    "pseudo": str,
    "password": str
}
```