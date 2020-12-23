from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models

class UserProfileAdmin(ImportExportModelAdmin):
    pass

class OrganizationAdmin(ImportExportModelAdmin):
    pass

admin.site.register(models.Organization,OrganizationAdmin)
admin.site.register(models.UserProfile,UserProfileAdmin)
admin.site.register(models.MemberUpload)
