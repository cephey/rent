# coding:utf-8
from django.http import JsonResponse
from django.views.generic import View


class JSONView(View):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return kwargs

    def render_to_response(self, context):
        return JsonResponse(context)
