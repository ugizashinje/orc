from django.contrib import admin

# Register your models here.
from django.core import serializers
from django.http import HttpResponse

from .models import Server, Image, ServerRequest, CloudService, CloudServiceProperty

def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", Server.objects.get(id=2), stream=response)
    return response

class ServerAdmin(admin.ModelAdmin):
    fields = ('cloud_id', 'status')
    list_display = ('id', 'name', 'cloud_id', 'status')
    actions = [export_as_json]
class CloudServicePropertyAdmin(admin.ModelAdmin):
    fields = ('name','value', 'cloud_service')
    list_display = ('name', 'value', 'cloud_service')


admin.site.register(Server, ServerAdmin)
admin.site.register(Image)
admin.site.register(ServerRequest)

admin.site.register(CloudService)
admin.site.register(CloudServiceProperty, CloudServicePropertyAdmin)