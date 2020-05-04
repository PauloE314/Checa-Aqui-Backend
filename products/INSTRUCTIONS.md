# Products

### **PATH:** ``` /products/ ``` - GET
#### (Autenticação não necessária)
#### GET:
Retorna a lista de produtos e informações adicionais simples. A pesquisa pode ser filtrada no query_params pelo **name** e pelo **product_type**.
<small> Por algum motivo, quando procurar por product_name é preciso retirar a ultima barra </small>

```base_url/products/?product_type=CELULAR ```
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Galaxy A10",
            "product_type": "CELULAR",
            "url_image": "lorem.com"
        },
        {
            "name": "Galaxy A20",
            "product_type": "CELULAR",
            "url_image": "lorem_3.com"
        },
        {
            "name": "Iphone 11",
            "product_type": "CELULAR",
            "url_image": "lorem_2.com"
        }
    ]
}
```

<hr>

### **PATH:** ``` /products/types ``` - GET
#### (Autenticação não necessária)
#### GET:
Retorna a lista de tipos de produtos.

<hr>

### **PATH:** ``` /products/stores ``` - GET
#### (Autenticação não necessária)
#### GET:
Retorna a lista de lojas atualmente.

<hr>


### **PATH:** ``` /products/detail/ ``` - GET
#### (Autenticação não necessária)
#### GET:
Retorna informações sobre um produto em específico. Dentre as informações, tem a lista de reviews sobre o produto em questão.

```json
{
    "name": "Armário",
    "product_type": "MÓVEL",
    "url_image": "lorem_6.com",
    "reviews": [
        {
            "id": 10,
            "likes": 0,
            "formated_store": [
                "AMER",
                "AMERICANAS"
            ],
            "description": "Gostei paks",
            "grade": 4.8,
            "product": "Armário",
            "author": {
                "id": 1,
                "username": "Admin",
                "profile": {
                    "email": "admin@admin.com",
                    "score": 3.0,
                    "points": 305,
                    "is_premium": false
                }
            }
        }
    ]
}
```

Para realizar a pesquisa, é necessário enviar o produto em questão pelos query_params na url:

``` base_url/products/detail/?product=Armário/ ```
