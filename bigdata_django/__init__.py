# 代码位置：first_django_app/__init__.py
from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

from .celery import app as celery_app

