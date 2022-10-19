from .models import Profile
from rest_framework import permissions

# Logging Stuff
import logging

_logger = logging.getLogger(__name__)
logger_name = str(_logger).upper()


class IsMerchant(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        p = Profile.objects.get(user=user)
        _logger.info(logger_name + ":-" + user.username + 'was trying to access something which requires IsMerchant '
                                                          'Permission')
        return user and p.role == 1


class IsConsumer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        p = Profile.objects.get(user=user)
        _logger.info(
            logger_name + ":-" + user.username + ' was trying to access something which requires IsConsumer Permission')
        return user and p.role == 2
