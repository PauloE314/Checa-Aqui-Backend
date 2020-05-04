from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from attendance.models import Attendance

class IsMainUser(BasePermission):
    message = 'O usuário não é o dono do perfil'

    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs['pk']

        try:
            main_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return True

        return request.user == main_user

class IsInAttendance(BasePermission):
    message = 'O usuário não está autorizado a ver esse atendimento'

    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs['pk']

        try:
            attendance = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return True
        return request.user == attendance.attendant or request.user == attendance.client


class IsClient(BasePermission):
    message = 'O usuário não está autorizado a avaliar esse atendimento como cliente'

    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs['pk']

        try:
            attendance = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return True
        return request.user == attendance.client


class IsAttendant(BasePermission):
    message = 'O usuário não está autorizado a avaliar esse atendimento como atendente'

    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs['pk']

        try:
            attendance = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return True
        return request.user == attendance.attendant


class GetOnly(BasePermission):
    message = 'A página está disponível apenas para visualização'

    def has_permission(self, request, view):        
        return request.method == 'GET'

class PutOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'PUT'

class PostOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'

class DeleteOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'DELETE'
