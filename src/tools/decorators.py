# coding:utf-8
from django.http import HttpResponseBadRequest
from functools import wraps


def ajax_required(f):
    """
    AJAX request required decorator
    @ajax_required
    def my_view(request):
    ....
    """
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    return wrapper
