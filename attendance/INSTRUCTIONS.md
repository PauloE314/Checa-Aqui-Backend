# Attendance

### **PATH:** ``` /attendance/client ``` - GET, POST
#### (Autenticação necessária)
#### GET:
Retorna a lista dos atendimentos em que o usuário foi o cliente.

``` json
{
    "count":1,
    "next":null,
    "previous":null,
    "results":
    [
        {
            "id":7,
            "client_can_evaluate":false,
            "attendant_can_evaluate":false,
            "min_time_to_client_evaluate":"2020-05-02T15:39:36.262215",
            "max_time_to_client_evaluate":"2020-05-03T15:33:36.262215",
            "max_time_to_attendant_evaluate":"2020-05-03T21:33:36.262215",
            "created_at":"2020-05-02T15:33:36.262215",
            "client_score":4,
            "attendant_score":4,
            "attendant_was_evaluated":true,
            "client_was_evaluated":true,
            "client":
            {
                "id":12,
                "username":"normal_user",
                "profile":
                {
                    "email":"normal_user@gmail.com",
                    "score":3.25,
                    "points":105,
                    "is_premium":false
                }
            },
            "attendant":
            {
                "id":21,
                "username":"email_user",
                "profile":
                {
                    "email":"pauloeduardodelima155@gmail.com",
                    "score":3.25,
                    "points":500,
                    "is_premium":false
                }
            },
            "product":"Galaxy A10"
        }
    ]
}
```
#### POST:

Cria um atendimento (na prática, o cliente solicita um atendimento).
Quando o atendimento é criado, o atendente solicitado recebe um email com informações sobre o cliente. Como resposta ao método, retorna o número de contato do cliente, que em outros momentos é invisível.

Envio:
```json
{
    "attendant": 1,
    "product": "Armário"
}
```

Email:
```
example1 solicita seu atendimento especializado sobre o produto Armário. Você tem 24 horas para respondê-lo na plataforma de comunicação que desejar. Telefone para contato: 8888888 
```


<hr>

### **PATH:** ``` /attendance/attendant ``` - GET
#### (Autenticação necessária)
#### GET:
Retorna a lista dos atendimentos em que o usuário foi o atendente. (Ver seção anterior)

<hr>

### **PATH:** ``` /attendance/(int:pk) ``` - GET
#### (Autenticação e ser cliente ou atendente do atendimento é necessário)
#### GET:
Retorna informações sobre um atendimento em específico.

### **PATH:** ``` /attendance/(int:pk)/client-avaliate/ ``` - PUT
#### (Autenticação e ser o cliente do atendimento é necessário)
#### PUT:
Se o cliente (o usuário) ainda não tiver avaliado o atendente a ainda estiver no prazo (é retornado com um get na url anterior), permite a avaliação do atendente por parte do cliente.

```json
{
    "score": 4.3
}
```

Ao ser avaliado, o atendente vai receber seus pontos.

<hr>

### **PATH:** ``` /attendance/(int:pk)/attendant-avaliate/ ``` - PUT
#### (Autenticação e o atendente do atendimento é necessário)
#### PUT:

Se o atendente (o usuário) ainda não tiver avaliado o cliente, o cliente já tiver avaliado o atendente e ainda estiver no prazo, permite a avaliação do cliente por parte do atendente.

```json
{
    "score": 4.3
}
```

Ao ser avaliado, o cliente vai receber seus pontos.
