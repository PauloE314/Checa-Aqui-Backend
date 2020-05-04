# API - **Checa Aqui**


## Dependências:

- Django: ``` pip install django ```
- Django Rest Framework: ``` pip install djangorestframework ```

- Django Cors Headers: ``` pip install django-cors-headers ```

- Psycopg: ``` pip install psycopg2 ```

O funcionamento da API é dividido em três seções de manipulação de dados (users, products, reviews); e segue o modelo padrão de API rest.

## Seções:
- [Users](users/INSTRUCTIONS.md) 

- [Products](products/INSTRUCTIONS.md)

- [Reviews](reviews/INSTRUCTIONS.md)

- [Attendance](attendance/INSTRUCTIONS.md)

É importante frisar que a lista de produtos está mantida dentro de um aquivo json na raíz do backend (products.json). Para atualizar os produtos automaticamente, execute o código com a venv:

``` bash
$ python manage.py load_products
```

<!-- │
├
└
─ -->
## URLS:

```
.
│
├─ /users
│     ├─ /token-login/
│     ├─ /authenticate-email/
│     ├─ /self/
│     ├─ /(int:pk)/
│     └─ /
├─ /products
│     ├─ /types/
│     ├─ /stores/
│     ├─ /detail/
│     └─ /
├─ /reviews
│     ├─ /like/(int:pk)
│     ├─ /self/
│     ├─ /(int:pk)/
│     └─ /
└─ /attendance
      ├─ /all/ <- Teste
      ├─ /client/
      ├─ /attendant/
      ├─ /(int:pk)/
      ├─ /(int:pk)/client-avaliate
      └─ /(int:pk)/attendant-avaliate
```

<small>Algumas constantes estão definidas no config.py, coisas como o tempo mínimo para o cliente avaliar o atendente, tempo máximo, tempo máximo do atendente, lojas, etc</small>
