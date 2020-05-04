import json
import os

from backend.settings import BASE_DIR
# from config import RELOAD_PRODUCTS_AUTO
from products.models import Product
# name=NAME; product_type = TYPE; score = 0 

def load():
    print('Atualizando produtos...')

    LIST = list()
    queryset = Product.objects.all()
    change = False
    names = list()


    product_structure_path = os.path.join(BASE_DIR, 'products.json')

    with open(product_structure_path, encoding="utf-8") as product_json:
        data = json.load(product_json)

    for _type, _list in data.items():
        for product in _list:
            obj, created_product = Product.objects.get_or_create(
                name=product['name']
            )

            names.append(product['name'])
            
            if created_product:
                obj.update(
                    product_type = _type,
                    url_image = product['image']
                )
                change = True
                print(f"Novo produto: ({obj})")
            
            else:
                if obj.product_type != _type:
                    change = True
                    print(f'Tipo de produto inexistente: ({obj.product_type}). Alterando para ({_type})')

                    obj.update(product_type=_type)

                if obj.url_image != product['image']:
                    change = True
                    print(f'Mudança na imagem: ({obj.url_image}). Alterando para ({product["image"]})')

                    obj.update(url_image=product['image'])
    


    for product in queryset:
        if product.name not in names:
            change = True
            print(f'Deletando produto: ({product})')
            product.delete()

    if not change:
        print('Nenhuma mudança identificada')