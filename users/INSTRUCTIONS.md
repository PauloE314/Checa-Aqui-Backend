# Users

### **PATH:** ``` /users/ ``` - GET, POST
#### (Autenticação não necessária)

#### GET:
Retorna a lista de todos os usuários com paginação. A pesquisa pode ser customizada através dos query_params.<br>
<small>Por padrão a lista vai estar ordendada em ordem alfabética em função do username.</small>

- **/users/?name=(texto)** : <small>Busca por nome</small>

- **/users/?order=relevance** : <small>Ordenar em função dos pontos</small>

- **/users/?premium** : <small>Retorna os usuários Premium</small>

- **/users?page=(número)** : <small>Paginação</small>


``` json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "exemplo1",
            "profile": {
                "email": "exemplo1@gmail.com",
                "score": 3.0,
                "points": 305,
                "is_premium": false
            }
        },
        {
            "id": 2,
            "username": "exemplo2",
            "profile": {
                "email": "exemplo2@gmail.com",
                "score": 3.25,
                "points": 500,
                "is_premium": false
            }
        },
    ]
}
```

<hr>

#### POST:

Cria um novo usuário. O formato de usuário deve ser:

```json
{
    "username": "example",
    "password": "password",
    "profile": {
        "phone": "83 9 88888888",
        "email": "example@gmail.com"
    }
}
```

A resposta contem as informações em do novo usuário. Durante a criação do usuário, ele receberá um email com o token de autenticação para efetivamente permitir o login.

<hr>

### **PATH:** ``` /users/token-login``` - POST
#### (Autenticação não necessária)
#### POST:
Serve para realizar o login com o username e password padrão e receber um Token de identificação. O json de envio deve ser no modelo:

``` json
{
    "username": "example",
    "password": "password"
}
```

<hr>

### **PATH:** ``` /users/authenticate-email``` - POST

#### POST (Autenticação não necessária):
Autentica o usuário para permitir login.<br>
O json de envio deve ser no modelo:

```json
{
    "token": "SADJGDIGOIOIRGIKGHOH2151AS5DF515"
}
```

<hr>

### **PATH:** ``` /users/self``` - GET, PUT, DELETE
#### (Autenticação necessária)

#### GET:

Retorna as informações do próprio usuário.

#### PUT:

Atualiza o perfil, seja por inteiro, ou parcialmente.

```json
inteiro:
{
    "id": 0,
    "username": "new_username",
    "password": "lorem_ipsum_dolor_amet",
    "profile":{
        "phone": "9 8888 8888",
        "email": "example@email.com",
        "score": -1
    }
}

parcial:
{
    "username": "new_username"
}
```

#### DELETE:

Esse método não requer nenhum dado, basta utilizá-lo e o usuário será deletado.

<hr>

### **PATH:** ``` /users/(int:pk)``` - GET 
#### (Autenticação não necessária)

#### GET:
Retorna as informações de outro usuário (que possui o id da URL). As reviews do usuário também são incluida.

```json
{
    "id": 1,
    "username": "exemplo",
    "profile": {
        "email": "exemplo1@gmailadmin.com",
        "score": 3.0,
        "points": 305,
        "is_premium": false
    },
    "reviews": [
        {
            "id": 1,
            "likes": 0,
            "formated_store": [
                "AMER",
                "AMERICANAS"
            ],
            "description": "Lorem ipsum",
            "grade": 3.5,
            "product": "Galaxy A10"
        },
        {
            "id": 9,
            "likes": 1,
            "formated_store": [
                "AMER",
                "AMERICANAS"
            ],
            "description": "lorem ipsum",
            "grade": 3.8,
            "product": "Cama"
        }
    ]
}

```
