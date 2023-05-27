from django.contrib import admin
from django.contrib import messages
# Register your models here.
admin.site.site_title = "数据查重平台"
admin.site.site_header = "数据查重平台"
from django.utils.html import format_html

from .tasks import do_single_data_diff
from django.core import serializers
from . models import Deduplication, Diffclum, Origclum


class Origdata_admin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['name']





class Deduplication_admin(admin.ModelAdmin):
    list_display = ['id', 'taskname', "raw_data", 'url', 'status', 'error', 'task_done', 'create_date', 'update_date']
    list_display_links = ['taskname']
    # readonly_fields = ["out_data", 'status', 'error', 'task_done', 'create_date', 'update_date', 'doituser']
    list_per_page = 10
    actions = ['do_data_diff']

    filter_horizontal = ['origdata', 'DiffData']


    def url(self, obj):
        if obj.status is True:
            return format_html('<a  target="_blank" href="/images/%s/">立即下载</a>' % (obj.out_data))
        else:
            return format_html('<a  target="_blank">任务执行中</a>')

    # def has_add_permission(self, request):
    #     return  False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False

    def do_data_diff(self, request, queryset):

        if len(queryset) > 1:

            messages.error(request, 'error ')
        else:
            # queryset[0].status =True
            queryset[0].save()
            data = serializers.serialize('json', queryset)

            do_single_data_diff.delay(data=data)

    def get_queryset(self, request):
        qs = super(Deduplication_admin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(doituser=request.user)


    def save_model(self, request, obj, form, change):
        obj.doituser = request.user
        super().save_model(request, obj, form, change)



    do_data_diff.short_description = '立即分析'
    url.short_description = '动作'
    # icon，参考element-ui icon与https://fontawesome.com
    do_data_diff.icon = 'fas fa-audio-description'

    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    do_data_diff.type = 'danger'


admin.site.register(Deduplication, Deduplication_admin)
admin.site.register(Origclum, Origdata_admin)
admin.site.register(Diffclum, Origdata_admin)
