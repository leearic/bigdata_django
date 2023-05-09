from django.apps import AppConfig


class DataDeduplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_deduplication'
    verbose_name = "数据去重"