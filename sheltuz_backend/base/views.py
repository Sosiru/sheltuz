# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.db import connection
from django.http import JsonResponse


class HealthCheckView(View):
    """
    Health check endpoint to confirm if the site is up and db is reachable.
    """
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            one = cursor.fetchone()[0]
        return JsonResponse({"success": True, "db": one})
