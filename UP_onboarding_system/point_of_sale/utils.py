import time
import structlog

logger = structlog.get_logger(__name__)
log = logger.new()
logger_name = str(logger).upper()


def log_db_queries(f):
    from django.db import connection
    def new_f(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        log.info("db queries log for %s:\n" % (f.__name__))
        log.info(" TOTAL COUNT : % s " % len(connection.queries))
        for q in connection.queries:
            log.info("%s: %s\n" % (q["time"], q["sql"]))
        end_time = time.time()
        duration = end_time - start_time
        log.info('\n Total time: {:.3f} ms'.format(duration * 1000.0))
        return res

    return new_f
