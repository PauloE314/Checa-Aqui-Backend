from rest_framework import serializers
from attendance.models import Attendance
from users.serializers import UserSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('attendant_score', 'client_score', 'attendant_was_evaluated', 'client_was_evaluated')

    client_can_evaluate = serializers.BooleanField(read_only=True)
    attendant_can_evaluate = serializers.BooleanField(read_only=True)

    min_time_to_client_evaluate = serializers.DateTimeField(read_only=True)
    max_time_to_client_evaluate = serializers.DateTimeField(read_only=True)
    max_time_to_attendant_evaluate = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        if validated_data['client'] == validated_data['attendant']:
            raise serializers.ValidationError({'attendant': 'O atendente precisa ser diferente do cliente'})
        else:
            new_attendance = Attendance.objects.create(
                client=validated_data['client'],
                attendant=validated_data['attendant'],
                product=validated_data['product']
            )

            return new_attendance


    def to_representation(self, instance):
        representation = super(AttendanceSerializer, self).to_representation(instance)
        representation['client'] = self.get_client(instance)
        representation['attendant'] = self.get_attendant(instance)
        return representation

    def get_client(self, instance):
        client = instance.client
        client_serializer = UserSerializer(client)
        return client_serializer.data

    def get_attendant(self, instance):
        attendant = instance.attendant
        attendant_serializer = UserSerializer(attendant)
        return attendant_serializer.data