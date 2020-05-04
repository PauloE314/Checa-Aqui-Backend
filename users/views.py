from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from users.serializers import UserSerializer, ProfileSerializer
from reviews.serializers import ReviewSerializer, ReviewSerializer_WithoutAuthorData

from rest_framework.authtoken.models import Token
from functions import send_validation
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from permissions import IsMainUser, GetOnly

from functions import send_validation, send_attendance_start_email



class Users(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        order = self.request.query_params.get('order', None)
        is_premium = self.request.query_params.get('premium', None)

        queryset = self.queryset.all()

        if name != None:
            queryset = User.objects.all().filter(username__icontains=name)

        if is_premium != None:
            queryset = queryset.filter(profile__is_premium=True)

        if order == 'relevance':
            queryset = list(reversed(sorted(queryset, key=lambda user: ((user.profile.score)*100 + user.profile.points) / 2)))
        else:
            queryset = queryset.order_by('username')

        return queryset

    def create(self, request):
        data = request.data

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            new_user = User.objects.get(username=data['username'])

            user_token = Token.objects.get(user=new_user).key
            encoded_token = urlsafe_base64_encode(force_bytes(user_token))

            send_validation(data['profile']['email'], encoded_token)

            return Response({'message': 'Criado com sucesso', **serializer.data})
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#    http_method_names = ['get', 'put', 'delete']

class DetailUsers(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        user_serializer = UserSerializer(user)

        user_reviews = user.reviews.all()
        reviews_serializer = ReviewSerializer_WithoutAuthorData(user_reviews, many=True).data


        return Response({
                **(user_serializer.data),
                'reviews': reviews_serializer
            }
        )




class DetailSelf(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'put', 'delete']

    def get_object(self):
        # user = User.objects.all()[0]
        user = self.request.user
        return user

    
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        user_serializer = UserSerializer(user)

        user_reviews = user.reviews.all()
        reviews_serializer = ReviewSerializer_WithoutAuthorData(user_reviews, many=True).data

                
        return Response({
                **(user_serializer.data),
                'reviews': reviews_serializer
            }
        )
        


    def put(self, request, *args, **kwargs):
        profile_update = {}
        profile_fields = ProfileSerializer.Meta().fields

        if 'profile' not in request.data:
            for field in request.data:
                if field in profile_fields:
                    profile_update[field] = request.data[field]

        if profile_update:
            try:
                profile = User.objects.get(pk=kwargs['pk']).profile
            except User.DoesNotExist:
                return Response({'erro': 'usuário inválido'}, status=status.HTTP_404_NOT_FOUND)

            serializer_profile = ProfileSerializer(profile, data=profile_update, partial=True)

            if serializer_profile.is_valid():
                serializer_profile.save()
            else:
                return Response(serializer_profile.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.partial_update(request, *args, **kwargs)


class ActiveAccount(APIView):
    def post(self, request):
        try: 
            enc_token = request.data.get('token')
            if enc_token:
                token = force_text(urlsafe_base64_decode(enc_token))  
                
                user = Token.objects.get(key=token).user
            else:
                return Response({'message': 'Dados inválidos'}, status=status.HTTP_400_BAD_REQUEST)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist, Token.DoesNotExist):  
              return Response({'message': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True  
        user.save()  
        return Response({'message': 'Email autenticado'})
