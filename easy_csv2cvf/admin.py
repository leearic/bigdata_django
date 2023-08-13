from django.contrib import admin
from . models import CsvFiles

from django.core import serializers
from django.contrib import messages
from .tasks import do_data_diff
class CsvFiles_admin(admin.ModelAdmin):
    list_display = ['id', 'task_name', 'status', 'out_data', 'task_done', 'errorlog', 'create_date']
    list_display_links = ['task_name']
    readonly_fields = ['out_data']
    actions = ['do_data_diff']
    def do_data_diff(self, request, queryset):

        if len(queryset) > 1:
            messages.error(request, 'error, only 1 task allowed per time')
        else:
            for ii in queryset:
                ii.status = True
                ii.save()
            data = serializers.serialize('json', queryset)
            do_data_diff.delay(data=data)
    do_data_diff.short_description = '立即分析'

    # icon，参考element-ui icon与https://fontawesome.com
    do_data_diff.icon = 'fas fa-audio-description'

    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    do_data_diff.type = 'danger'

admin.site.register(CsvFiles, CsvFiles_admin)