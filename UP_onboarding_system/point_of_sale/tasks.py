from .models import *
from celery import shared_task
from .serializers import *
from celery.utils.log import get_task_logger
from time import sleep
import logging
import structlog

# _logger = logging.getLogger(__name__)
# logger_name = str(_logger).upper()

#loggerr = structlog.get_logger(__name__)


@shared_task()
def create_an_order(pk, data):
    #import ipdb; ipdb.set_trace()
    # print("CELERY SSSSSSSSSSSSSSSSSS")
    #_logger.info("CELERY Start")
    # sleep(5)
    serializer = OrderSerializer(data=data)
    user = User.objects.get(pk=pk)
    serializer.is_valid()
    serializer.save(user=user)
    return True
    #return serializer
    # _logger.info("CELERY Worked")
    # print("CELERY worked SSSSSSSSSSSSSSSSSSSSS")
