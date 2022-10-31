from .models import *
from celery import shared_task
from .serializers import *
from celery.utils.log import get_task_logger
from time import sleep
import logging
import structlog
from urllib import response
from .models import *
from celery import Celery
from .serializers import *
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response


# _logger = logging.getLogger(__name__)
# logger_name = str(_logger).upper()

# loggerr = structlog.get_logger(__name__)


# @shared_task()
# def create_an_order(pk, data):
#     #import ipdb; ipdb.set_trace()
#     # print("CELERY SSSSSSSSSSSSSSSSSS")
#     #_logger.info("CELERY Start")
#     # sleep(5)
#     serializer = OrderSerializer(data=data)
#     user = User.objects.get(pk=pk)
#     serializer.is_valid()
#     serializer.save(user=user)
#     #return True
#     #return serializer
#     # _logger.info("CELERY Worked")
#     # print("CELERY worked SSSSSSSSSSSSSSSSSSSSS")

@shared_task()
def create_store(user, data):
    user = User.objects.get(pk=user)
    profile = Profile.objects.get(user=user)
    serializer = StoresSerializer(data=data)
    valid = serializer.is_valid(raise_exception=True)
    if valid:
        serializer.save(merchant=profile)
        return valid
    else:
        response = {
            'success': True,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': "Error in Store Creation"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@shared_task()
def create_an_order(user, data):
    user = User.objects.get(pk=user)
    serializer = OrderSerializer(data=data)
    valid = serializer.is_valid(raise_exception=True)
    if valid:
        serializer.save(user=user)
        return valid
    else:
        response = {
            'success': True,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': "Error in Order Creation"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
