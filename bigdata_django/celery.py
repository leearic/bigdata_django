from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# 设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigdata_django.settings")

#创建celery应用
app = Celery('bigdata_django')
app.config_from_object('django.conf:settings')

app.conf.CELERY_TIMEZONE = 'Asia/Shanghai'
app.conf.BROKER_URL = 'redis://127.0.0.1:6379/0'
# app.conf.BROKER_TRANSPORT = 'redis://127.0.0.1:6379/0'
app.conf.CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # BACKEND配置，这里使用redis
# app.conf.CELERY_RESULT_SERIALIZER = 'json'
app.conf.CELERY_IMPORTS = ('data_deduplication.tasks')

app.conf.CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  ###

app.conf.CELERY_WORKER_CONCURRENCY = 1
app.conf.CELERY_WORKER_MAX_TASKS_PER_CHILD = 200
# app.conf.CELERY_TASK_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
app.conf.CELERY_TASK_SERIALIZER = 'json'
app.conf.CELERY_RESULT_SERIALIZER = 'json'

#如果在工程的应用中创建了 tasks.py 模块，那么Celery应用就会自动去检索创建的任务。
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)