from .models import Profile
from rest_framework import permissions


class IsMerchant(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        p = Profile.objects.get(user=user)
        return user and p.role == 1


class IsConsumer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        p = Profile.objects.get(user=user)
        return user and p.role == 2
