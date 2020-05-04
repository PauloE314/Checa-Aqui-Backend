from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from permissions import GetOnly, IsClient, IsAttendant, IsInAttendance

from functions import send_attendance_start_email

from django.utils import timezone



class ClientAttendances(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = self.request.user.client_attendances.all()
        queryset = queryset.order_by('-id')
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        client = request.user
        
        data['client'] = client.id
        serializer = AttendanceSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            attendance = Attendance.objects.get(pk=serializer.data['id'])
            attendant = attendance.attendant
            send_attendance_start_email(attendance)

            return Response({'message': 'Criado com sucesso', 'attendant_phone': attendant.profile.phone, **(serializer.data)})
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AttendantAttendances(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = self.request.user.attendant_attendances.all()
        queryset = queryset.order_by('-id')
        return queryset


class DetailAttendances(generics.RetrieveAPIView):
    permission_classes = [IsInAttendance & IsAuthenticated]

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def retrieve(self, request, pk):
        try:
            instance = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return Response({'message': 'Atendimento inválido'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AttendanceSerializer(instance)

        return Response(serializer.data)

class Client_Evaluate_Attendant(generics.RetrieveUpdateAPIView):
    permission_classes = [IsClient & IsAuthenticated]

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        #Se o cliente pode avaliar
        if instance.client_can_evaluate:
            score = data.get('score', None)
            #Se tiver alguma avaliação
            if score:
                instance.evaluate_attendant(score)
                serializer = AttendanceSerializer(instance)
                return Response(serializer.data)
            else:
                return Response({'message': 'Dê uma nota ao atendente'}, status=status.HTTP_400_BAD_REQUEST)       
        else:

            if not instance.attendant_was_evaluated:
                # Se ainda não estiver no tempo mínimo
                if instance.min_time_to_client_evaluate > timezone.now():
                    return Response({'message': 'Ainda não foi atingido o tempo mínimo esperado'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                # Se já passou do tempo
                else:
                    return Response({'message': 'Já passou o praso da avaliação'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            # Se Já tiver sido avaliado
            else:
                return Response({'message': 'O atendente já foi avaliado'}, status=status.HTTP_406_NOT_ACCEPTABLE)



class Attendant_Evaluate_Client(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAttendant & IsAuthenticated]

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # Se o atendente puder avaliar
        if instance.attendant_can_evaluate:
            score = data.get('score', None)
            if score:
                instance.evaluate_client(score)
                serializer = AttendanceSerializer(instance)
                return Response(serializer.data)

            else:
                return Response({'message': 'Dê uma nota ao Cliente'}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            if not instance.client_was_evaluated:
                #Se o cliente ainda não avaliou o cara
                if instance.client_can_evaluate:
                    return Response({'message': 'O cliente ainda não avaliou você'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                # Se já tiver passado do prazo de avaliação do cliente
                else:
                    return Response({'message': 'Já passou o praso da avaliação'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            # Se o atendimento já tiver sido avaliado
            else:
                return Response({'message': 'O cliente já foi avaliado'}, status=status.HTTP_406_NOT_ACCEPTABLE)