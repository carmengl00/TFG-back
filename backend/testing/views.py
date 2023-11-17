import logging

from django.http import HttpResponse

logger = logging.getLogger(__name__)


def healthcheck_ok(request):
    """Simple 200 code response (i.e. health check)"""
    logger.info("Test OK")
    return HttpResponse("OK")


def raise_error(request):
    """View for testing 500 errors"""

    msg = "Error raised for testing purposes"
    logger.error(msg)
    raise Exception(msg)
