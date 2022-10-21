from .models import Profile
from rest_framework import permissions

# Logging Stuff
# import logging
import structlog

# _logger = logging.getLogger(__name__)
# logger_name = str(_logger).upper()
_logger = structlog.get_logger(__name__)
logger_name = str(_logger).upper()


def return_role(user):
    p = Profile.objects.get(user=user)
    if p.role == 1:
        role = "Merchant"
    elif p.role == 2:
        role = "Customer"
    return role


class IsMerchant(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        p = Profile.objects.get(user=user)
        # _logger.info(logger_name + ":-" + user.username + 'was trying to access something which requires IsMerchant '
        #                                                   'Permission')
        _logger.info(event='Permissions !', user=user.username, role=return_role(user),
                     message='was trying to access something which requires IsMerchant Permission')
        return user and p.role == 1


class IsConsumer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        p = Profile.objects.get(user=user)
        # _logger.info(
        #     logger_name + ":-" + user.username + ' was trying to access something which requires IsConsumer Permission')
        _logger.info(event='Permissions !', user=user.username, role=return_role(user),
                     message='was trying to access something which requires IsConsumer Permission')
        return user and p.role == 2
