from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'

    def ready(slef):
        from config import RELOAD_PRODUCTS_AUTO

        if RELOAD_PRODUCTS_AUTO:
            from products import product_update