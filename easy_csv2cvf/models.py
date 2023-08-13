from django.db import models
import datetime
import uuid
general = uuid.uuid1()

# Create your models here.
def user_directory_path(instance, filename):
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d')
    return 'upload/{0}/{1}/{2}'.format(nowtime, general, filename)



class CsvFiles(models.Model):
    '''
        数据去重
    '''
    task_name = models.CharField(max_length=255, verbose_name="TaskName", help_text='TaskName')
    raw_data = models.FileField(verbose_name="RowData", help_text='RowData', upload_to=user_directory_path)
    out_data = models.FileField(verbose_name="OutVcf", help_text='OutVcf', null=True, blank=True)
    status = models.BooleanField(verbose_name="状态", help_text='状态', default=False)
    task_done = models.BooleanField(verbose_name="任务", help_text='任务', default=False)
    errorlog = models.TextField(default='Nul')
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = u'CvfTask'
        verbose_name_plural = u'CvfTask'
        ordering = ['-id']

    def __str__(self):
        return 'CvfTask: ' + str(self.task_name)