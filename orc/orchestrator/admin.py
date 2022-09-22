from django.contrib import admin

# Register your models here.
from .models import Server, Image, ServerRequest, CloudService, CloudServiceProperty

class ServerAdmin(admin.ModelAdmin):
    fields = ('cloud_id', 'status')
    list_display = ('id', 'name', 'cloud_id', 'status')

class CloudServicePropertyAdmin(admin.ModelAdmin):
    fields = ('name','value', 'cloud_service')
    list_display = ('name', 'value', 'cloud_service')


admin.site.register(Server, ServerAdmin)
admin.site.register(Image)
admin.site.register(ServerRequest)

admin.site.register(CloudService)
admin.site.register(CloudServiceProperty, CloudServicePropertyAdmin)