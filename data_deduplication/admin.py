from django.contrib import admin
from django.contrib import messages
# Register your models here.
admin.site.site_title = "数据查重平台"
admin.site.site_header = "数据查重平台"
from django.utils.html import format_html

from .tasks import  do_data_diff
from django.core import serializers
from . models import Deduplication

class Deduplication_admin(admin.ModelAdmin):
    list_display = ['id', 'taskname', "raw_data", 'comparative_data', 'url', 'status', 'error', 'task_done', 'create_date']
    list_display_links = ['taskname']
    # list_filter = ['hostname',]
    # search_fields = ['hostname', ]
    list_per_page = 10
    actions = ['do_data_diff']
    def url(self, obj):
        if obj.status is True:
            return format_html('<a  target="_blank" href="/images/%s/">下载文件</a>' % (obj.out_data))
        else:
            return format_html('<a  target="_blank">任务执行中</a>')

    # def has_add_permission(self, request):
    #     return  False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def do_data_diff(self, request, queryset):

        if len(queryset) > 1:
            messages.error(request, 'error ')
        else:
            data = serializers.serialize('json', queryset)
            do_data_diff.delay(data=data)




    do_data_diff.short_description = '测试按钮'
    url.short_description = 'download'
    # icon，参考element-ui icon与https://fontawesome.com
    do_data_diff.icon = 'fas fa-audio-description'

    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    do_data_diff.type = 'danger'


admin.site.register(Deduplication, Deduplication_admin)