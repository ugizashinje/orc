import orchestrator.constants
from django.db import models


class Image(models.Model):
    cloud_id = models.CharField(blank=None, null=False, max_length=64)

    def __str__(self):
        return self.cloud_id


class InstanceType(models.Model):
    name = models.CharField(null=False, blank=False, max_length=64)

    def __str__(self):
        return self.name


class CloudService(models.Model):
    name = models.CharField(blank=False, null=False, default='', max_length=64)
    def __str__(self):
        return self.name


class Server(models.Model):
    cloud_id = models.CharField(blank=True, null=True, max_length=64)
    cloud_service = models.ForeignKey(CloudService, on_delete=models.CASCADE, null=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=False)
    status = models.CharField(blank=False, choices=orchestrator.constants.Server.Status.ADMIN_CHOICES, max_length=16)
    name = models.CharField(blank=False, null=False, default='', max_length=128)
    instance_type = models.ForeignKey(InstanceType, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ServerRequest(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    body = models.JSONField(default=dict, null=False, blank=False)
    name = models.CharField(blank=False, null=False, max_length=256, default="")


class CloudServiceProperty(models.Model):
    cloud_service = models.ForeignKey(CloudService, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=64)
    value = models.CharField(null=True, blank=True, max_length=64)

    class Meta:
        verbose_name_plural = 'CloudServiceProperties'
