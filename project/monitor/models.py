# system_monitor/monitor/models.py
from django.db import models

class SystemMetrics(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.FloatField()
    ram_usage = models.FloatField()
    disk_usage = models.FloatField()
    is_monitoring = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']