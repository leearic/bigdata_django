import datetime

from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import User
general = uuid.uuid1()

def user_directory_path(instance, filename):
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d')
    return 'upload/{0}/{1}/{2}'.format(nowtime, general, filename)

class Deduplication(models.Model):
    '''
        数据去重
    '''
    taskname = models.CharField(max_length=255, verbose_name="任务名称", help_text='任务名称')
    raw_data = models.FileField(verbose_name="原始数据", help_text='原始数据', upload_to=user_directory_path)
    comparative_data = models.FileField(verbose_name="去重数据", help_text='去重数据', upload_to=user_directory_path)
    out_data = models.FileField(verbose_name="去重的数据", help_text='去重的数据', upload_to=user_directory_path, null=True, blank=True)
    status = models.BooleanField(verbose_name="状态", help_text='状态', default=False)
    error = models.BooleanField(verbose_name="错误", help_text='错误', default=False)
    task_done = models.BooleanField(verbose_name="任务", help_text='任务', default=False)
    doituser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = u'数据去重'
        verbose_name_plural = u'数据去重'
        ordering = ['-id']

    def __str__(self):
        return '数据去重: 任务名称-' + str(self.taskname)