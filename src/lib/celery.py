from celery import Celery


def make_celery(name, broker, imports=(), routes={}):
    celery = Celery(name, broker=broker, )
    celery.conf.update(
        CELERY_IMPORTS=imports,
        CELERY_ROUTES=routes
    )
    return celery