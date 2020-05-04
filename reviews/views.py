from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from reviews.models import Review
from reviews.serializers import ReviewSerializer, ReviewSerializer_WithoutAuthorData
from permissions import GetOnly, IsMainUser

class Reviews(generics.ListCreateAPIView):
    permission_classes = [GetOnly | IsAuthenticated]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


    def get_queryset(self):
        queryset = self.queryset.all()
        author = self.request.query_params.get('author', None)
        product = self.request.query_params.get('product', None)
        order = self.request.query_params.get('order', None)

        if author != None:
            queryset = queryset.filter(author__username__icontains=author)
        
        if product != None:
            queryset = queryset.filter(product__name__icontains=product)
        
        if order != None:
            if order == 'old':
                queryset = queryset.order_by('id')
    
            elif order == 'relevance':
                queryset = list(reversed(sorted(queryset, key=lambda rev: rev.likes)))
        else:
            queryset = queryset.order_by('-id')

        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.id

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            request.user.profile.set_points('REVIEW')

            return Response({'message': 'Review criado com sucesso', **(serializer.data)})
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SelfReviews(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer_WithoutAuthorData

    def get_queryset(self):
        user = self.request.user
        reviews = user.reviews.all().order_by('-id')
        return reviews

        

class DetailReview(generics.RetrieveDestroyAPIView):
    permission_classes = [IsMainUser | GetOnly]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class LikeReview(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        review_owner = instance.author
        serializer_class = self.get_serializer_class()

        if user not in instance.like_users.all():
            instance.like_users.add(user)
            review_owner.profile.set_points('LIKE')
        else:
            instance.like_users.remove(user)
            review_owner.profile.set_points('REMOVE_LIKE')

        serialized_review = serializer_class(instance)

        return Response(serialized_review.data)

