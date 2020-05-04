from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from products.models import Product
from products.serializers import ProductSerializer
from reviews.serializers import ReviewSerializer

from backend.settings import BASE_DIR
import json
import os
import config 


class Products(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        product_type = self.request.query_params.get('product_type', None)

        if name != None:
            queryset = Product.objects.filter(name__icontains=name)
        else:
            queryset = Product.objects.all()

        if product_type != None:
            queryset = queryset.filter(product_type__icontains=product_type)

        serializer_list = queryset.order_by('name')

        return  serializer_list


class DetailProducts(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request):
        name = request.GET.get('product')
        if name:
            try:
                product = Product.objects.get(name__icontains=name)
            except Product.DoesNotExist:
                return Response({'error': "Produto não cadastrado ou mal formatado"}, status=status.HTTP_404_NOT_FOUND)

            product_serializer = ProductSerializer(product)

            reviews = product.reviews.all()
            reviews_serializer = ReviewSerializer(reviews, many=True)

            return Response({**product_serializer.data, "reviews": reviews_serializer.data}) 
        else:
            return Response({'message': 'Keyword "product" não encontrado'}, status=status.HTTP_404_NOT_FOUND)


class ProductTypes(APIView):
    def get(self, request):
        product_structure_path = os.path.join(BASE_DIR, 'products.json')

        with open(product_structure_path, encoding="utf-8") as product_json:
            types = [_type for _type in json.load(product_json)]
            
        return Response({'types': types})


class Stores(APIView):
    def get(self, request):
        stores = config.STORES

        return Response({'stores': stores})